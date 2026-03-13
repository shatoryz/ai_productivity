import math
import time
import datetime
from database import db
from utils import get_current_time_minutes, is_time_in_range, get_session_id

AUDIO_WEIGHT = 0.3


class Engine:
    WEIGHTS = {'S': 0.40, 'E': 0.30, 'P': 0.20, 'C': 0.10}
    EMOTION_WEIGHTS = {
        'mental': {'neutral': 0.3, 'happy': 0.5, 'sad': -0.6, 'angry': -0.5, 'surprise': 0.1},
        'physical': {'neutral': 0.3, 'happy': 0.3, 'sad': -0.2, 'angry': 0.1, 'surprise': 0.2},
        'creative': {'neutral': 0.2, 'happy': 0.6, 'sad': -0.3, 'angry': -0.4, 'surprise': 0.5},
    }
    OPTIMAL_TIMES = {
        'mental': {'peak': 11, 'secondary': 15},
        'physical': {'peak': 17, 'secondary': 9},
        'creative': {'peak': 14, 'secondary': 20},
        'break': {'peak': 13, 'secondary': 18},
        'learning': {'peak': 10, 'secondary': 16},
    }

    def __init__(self, user_id, db_mgr):
        self.user_id = user_id
        self.db_mgr = db_mgr
        self.session_id = get_session_id()
        self.coefficients = self._load_coefficients()

    def _load_coefficients(self):
        conn = self.db_mgr.get_connection()
        cur = conn.cursor()
        cur.execute('SELECT * FROM user_coefficients WHERE user_id=?', (self.user_id,))
        result = cur.fetchone()
        if result:
            coeffs = {
                'w_S': float(result[5]) if result[5] else 0.4,
                'w_E': float(result[6]) if result[6] else 0.3,
                'w_P': float(result[7]) if result[7] else 0.2,
                'w_C': float(result[8]) if result[8] else 0.1,
                't_max_eyes': float(result[9]) if result[9] else 2.5,
                'f_opt_blink': float(result[10]) if result[10] else 17.0,
                'sigma_time': float(result[11]) if result[11] else 2.0,
                'cooldown_tau': float(result[12]) if result[12] else 45.0,
                'history_size': int(result[16]) if len(result) > 16 and result[16] else 10,
                'alpha': float(result[17]) if len(result) > 17 and result[17] else 0.1,
                'gamma': float(result[18]) if len(result) > 18 and result[18] else 0.15
            }
            conn.close()
            return coeffs
        else:
            cur.execute('INSERT INTO user_coefficients (user_id) VALUES (?)', (self.user_id,))
            conn.commit()
            conn.close()
            return self._default_coefficients()

    def _default_coefficients(self):
        return {
            'w_S': 0.4, 'w_E': 0.3, 'w_P': 0.2, 'w_C': 0.1,
            't_max_eyes': 2.5, 'f_opt_blink': 17.0,
            'sigma_time': 2.0, 'cooldown_tau': 45.0,
            'history_size': 10,
            'alpha': 0.1,
            'gamma': 0.15
        }

    def update_coefficients(self, new_coeffs):
        conn = self.db_mgr.get_connection()
        cur = conn.cursor()
        cur.execute('''UPDATE user_coefficients SET
            w_S=?, w_E=?, w_P=?, w_C=?, alpha=?, gamma=?
            WHERE user_id=?''',
                    (new_coeffs.get('w_S', self.coefficients['w_S']),
                     new_coeffs.get('w_E', self.coefficients['w_E']),
                     new_coeffs.get('w_P', self.coefficients['w_P']),
                     new_coeffs.get('w_C', self.coefficients['w_C']),
                     new_coeffs.get('alpha', self.coefficients.get('alpha', 0.1)),
                     new_coeffs.get('gamma', self.coefficients.get('gamma', 0.15)),
                     self.user_id))
        conn.commit()
        conn.close()
        self.coefficients.update(new_coeffs)
        return True

    def _clip(self, value, min_val=0.0, max_val=1.0):
        return max(min_val, min(max_val, value if value is not None else 0.0))

    def calculate_S(self, t_closed, f_blink, pose_angle):
        t_closed = t_closed if t_closed is not None else 0.0
        f_blink = f_blink if f_blink is not None else 0.0
        pose_angle = pose_angle if pose_angle is not None else 0.0
        S_eyes = self._clip(1.0 - (t_closed / self.coefficients['t_max_eyes']))
        S_blink = self._clip(f_blink / self.coefficients['f_opt_blink'])
        S_pose = self._clip(1.0 - (pose_angle / 90.0))
        return self._clip(S_eyes * 0.5 + S_blink * 0.3 + S_pose * 0.2)

    def calculate_E(self, emotion_probs, activity_category):
        emotion_probs = emotion_probs if emotion_probs else {'neutral': 1.0}
        weights = self.EMOTION_WEIGHTS.get(activity_category, self.EMOTION_WEIGHTS['mental'])
        E_raw = sum(emotion_probs.get(emo, 0.0) * weight for emo, weight in weights.items())
        audio_adjustment = AUDIO_WEIGHT * 0.1
        E_raw += audio_adjustment
        return self._clip(1.0 / (1.0 + math.exp(-E_raw)))

    def calculate_P(self, current_hour, activity_category):
        times = self.OPTIMAL_TIMES.get(activity_category)
        if not times:
            return 0.5
        sigma = self.coefficients['sigma_time']
        P_current = math.exp(-((current_hour - times['peak']) ** 2) / (2 * sigma ** 2))
        if 'secondary' in times:
            P_current = max(P_current, math.exp(-((current_hour - times['secondary']) ** 2) / (2 * sigma ** 2)))
        return self._clip(P_current)

    def calculate_C_factor(self, difficulty, S_adj):
        difficulty = difficulty if difficulty is not None else 0.5
        S_adj = S_adj if S_adj is not None else 0.5
        return self._clip((1.0 - difficulty) * S_adj)

    def calculate_score(self, S, E, P, C_factor, priority_time=1.0):
        base_score = (self.coefficients['w_S'] * S + self.coefficients['w_E'] * E +
                      self.coefficients['w_P'] * P + self.coefficients['w_C'] * C_factor)
        return base_score * priority_time

    def calculate_productivity_score(self, S, E, P, C):
        return (0.4 * S + 0.3 * E + 0.2 * P + 0.1 * C) * 100

    def calculate_trend(self, productivity_scores):
        if len(productivity_scores) < 6:
            return 0.0
        recent_3 = productivity_scores[-3:]
        old_3 = productivity_scores[:3]
        avg_recent = sum(recent_3) / len(recent_3)
        avg_old = sum(old_3) / len(old_3)
        trend = avg_recent - avg_old
        return self._clip(trend, -1.0, 1.0)

    def calculate_score_with_trend(self, productivity, trend):
        gamma = self.coefficients.get('gamma', 0.15)
        score_trend = productivity * (1 + gamma * trend)
        return self._clip(score_trend, 0.0, 100.0)

    def update_task_score_with_feedback(self, current_score, feedback):
        alpha = self.coefficients.get('alpha', 0.1)
        new_score = current_score + alpha * feedback
        return self._clip(new_score, 0.0, 100.0)

    def get_productivity_with_trend(self):
        factor_history = self.get_factor_history_for_charts()
        if not factor_history:
            return {'productivity': 0, 'trend': 0, 'score_trend': 0}
        productivity_scores = []
        for h in factor_history:
            S = h[0] if h[0] else 0
            E = h[1] if h[1] else 0
            P = h[2] if h[2] else 0
            C = h[3] if h[3] else 0
            score = self.calculate_productivity_score(S, E, P, C)
            productivity_scores.append(score)
        if not productivity_scores:
            return {'productivity': 0, 'trend': 0, 'score_trend': 0}
        current_productivity = productivity_scores[-1] if productivity_scores else 0
        trend = self.calculate_trend(productivity_scores)
        score_trend = self.calculate_score_with_trend(current_productivity, trend)
        return {
            'productivity': current_productivity,
            'trend': trend,
            'score_trend': score_trend,
            'avg': sum(productivity_scores) / len(productivity_scores),
            'best': max(productivity_scores),
            'sessions': len(productivity_scores)
        }

    def save_factor_history(self, S, E, P, C):
        conn = self.db_mgr.get_connection()
        cur = conn.cursor()
        cur.execute('''INSERT INTO factor_history
            (user_id, S_value, E_value, P_value, C_value, timestamp, session_id)
            VALUES (?, ?, ?, ?, ?, ?, ?)''',
                    (self.user_id, S, E, P, C, time.time(), self.session_id))
        conn.commit()
        conn.close()
        return True

    def save_trend_data(self, productivity, trend, score_trend):
        conn = self.db_mgr.get_connection()
        cur = conn.cursor()
        cur.execute('''INSERT INTO trend_history
            (user_id, productivity, trend, score_trend, timestamp, session_id)
            VALUES (?, ?, ?, ?, ?, ?)''',
                    (self.user_id, productivity, trend, score_trend, time.time(), self.session_id))
        conn.commit()
        conn.close()
        return True

    def save_session_productivity(self, productivity):
        conn = self.db_mgr.get_connection()
        cur = conn.cursor()
        cur.execute('''INSERT INTO session_productivity
            (user_id, session_id, productivity, timestamp)
            VALUES (?, ?, ?, ?)''',
                    (self.user_id, self.session_id, productivity, time.time()))
        conn.commit()
        conn.close()

    def get_session_productivity(self, limit=100):
        conn = self.db_mgr.get_connection()
        cur = conn.cursor()
        cur.execute('''SELECT productivity, timestamp
            FROM session_productivity
            WHERE user_id=? AND session_id=?
            ORDER BY timestamp ASC
            LIMIT ?''',
                    (self.user_id, self.session_id, limit))
        result = cur.fetchall()
        conn.close()
        return result if result else []

    def get_trend_history(self, limit=50):
        conn = self.db_mgr.get_connection()
        cur = conn.cursor()
        cur.execute('''SELECT productivity, trend, score_trend, timestamp
            FROM trend_history
            WHERE user_id=?
            ORDER BY timestamp ASC
            LIMIT ?''',
                    (self.user_id, limit))
        result = cur.fetchall()
        conn.close()
        return result if result else []

    def get_recommendation(self, user_state, available_activities, planned_time=30):
        if not available_activities:
            return None
        current_hour = user_state.get('current_hour', 12)
        current_mins = get_current_time_minutes()
        current_date = datetime.datetime.now().strftime('%Y-%m-%d')
        scheduled_activity = None
        for act in available_activities:
            act_date = act.get('scheduled_date')
            if act_date == current_date:
                if is_time_in_range(current_mins, act.get('start_time', '00:00'),
                                    act.get('end_time', '23:59')):
                    scheduled_activity = act
                    break
        S = self.calculate_S(
            user_state.get('t_closed', 0.0),
            user_state.get('f_blink', 0.0),
            user_state.get('pose_angle', 0.0)
        )
        emotion_probs = user_state.get('emotion_probs', {'neutral': 1.0})
        productivity_data = self.get_productivity_with_trend()
        current_trend = productivity_data.get('trend', 0)
        scored = []
        for act in available_activities:
            category = act.get('category', 'mental')
            E = self.calculate_E(emotion_probs, category)
            P = self.calculate_P(current_hour, category)
            C = self.calculate_C_factor(act.get('difficulty', 0.5), S)
            priority = act.get('priority', 0.5) * 2
            score = self.calculate_score(S, E, P, C, priority)
            score_with_trend = self.calculate_score_with_trend(score * 100, current_trend)
            if scheduled_activity and act['activity'] == scheduled_activity['activity']:
                score_with_trend *= 10
            scored.append({
                'activity': act,
                'score': score_with_trend,
                'base_score': score,
                'trend': current_trend,
                'is_scheduled': (scheduled_activity and act['activity'] == scheduled_activity['activity']),
                'factors': {'S': S, 'E': E, 'P': P, 'C': C}
            })
        scored.sort(key=lambda x: x['score'], reverse=True)
        best = scored[0]
        reasons = []
        if best.get('is_scheduled'):
            reasons.append('Scheduled now')
        if best['factors']['S'] > 0.8:
            reasons.append('Full energy')
        if best['factors']['E'] > 0.7:
            reasons.append('Great mood')
        if current_trend > 0.1:
            reasons.append('Improving trend')
        elif current_trend < -0.1:
            reasons.append('Declining trend')
        if not reasons:
            reasons.append('Balanced choice')
        self.save_factor_history(S, E, P, C)
        productivity = self.calculate_productivity_score(S, E, P, C)
        score_trend = self.calculate_score_with_trend(productivity, current_trend)
        self.save_trend_data(productivity, current_trend, score_trend)
        return {
            'activity': best['activity'],
            'score': best['score'],
            'trend': current_trend,
            'reason': ' | '.join(reasons[:3]),
            'all_scores': scored[:3],
            'planned_time': planned_time,
            'factors': best['factors'],
            'is_scheduled': best.get('is_scheduled', False)
        }

    def log_activity(self, category, duration_minutes, activity_name='Task'):
        conn = self.db_mgr.get_connection()
        cur = conn.cursor()
        cur.execute('''INSERT INTO activity_history
            (user_id, category, time_spent, last_time, date, activity_name)
            VALUES (?, ?, ?, ?, ?, ?)''',
                    (self.user_id, category, float(duration_minutes), time.time(),
                     datetime.date.today().isoformat(), activity_name))
        conn.commit()
        conn.close()
        return True

    def save_recommendation(self, activity, category, score, factors, planned_time):
        conn = self.db_mgr.get_connection()
        cur = conn.cursor()
        cur.execute('''INSERT INTO recommendation_history
            (user_id, activity, category, score, factors, timestamp, scheduled_time, completed)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)''',
                    (self.user_id, activity, category, float(score), str(factors),
                     time.time(), str(planned_time), 0))
        conn.commit()
        conn.close()
        return True

    def get_recommendation_history(self, limit=10):
        conn = self.db_mgr.get_connection()
        cur = conn.cursor()
        cur.execute('''SELECT activity, category, score, timestamp,
            scheduled_time, completed, feedback_score
            FROM recommendation_history
            WHERE user_id=? ORDER BY timestamp DESC LIMIT ?''',
                    (self.user_id, limit))
        result = cur.fetchall()
        conn.close()
        return result

    def clear_recommendation_history(self):
        conn = self.db_mgr.get_connection()
        cur = conn.cursor()
        cur.execute('DELETE FROM recommendation_history WHERE user_id=?', (self.user_id,))
        conn.commit()
        conn.close()
        return True

    def get_activity_stats(self):
        conn = self.db_mgr.get_connection()
        cur = conn.cursor()
        cur.execute('''SELECT category, SUM(time_spent) FROM activity_history
            WHERE user_id=? AND date=? GROUP BY category''',
                    (self.user_id, datetime.date.today().isoformat()))
        result = cur.fetchall()
        conn.close()
        return result

    def get_factor_history_for_charts(self, limit=100):
        conn = self.db_mgr.get_connection()
        cur = conn.cursor()
        cur.execute('''SELECT S_value, E_value, P_value, C_value, timestamp
            FROM factor_history
            WHERE user_id=?
            ORDER BY timestamp ASC
            LIMIT ?''',
                    (self.user_id, limit))
        result = cur.fetchall()
        conn.close()
        return result if result else []

    def get_productivity_stats(self):
        factor_history = self.get_factor_history_for_charts()
        if not factor_history:
            return {'avg': 0, 'trend': 0, 'best': 0, 'sessions': 0, 'score_trend': 0}
        productivity_scores = []
        for h in factor_history:
            S = h[0] if h[0] else 0
            E = h[1] if h[1] else 0
            P = h[2] if h[2] else 0
            C = h[3] if h[3] else 0
            score = self.calculate_productivity_score(S, E, P, C)
            productivity_scores.append(score)
        if not productivity_scores:
            return {'avg': 0, 'trend': 0, 'best': 0, 'sessions': 0, 'score_trend': 0}
        avg = sum(productivity_scores) / len(productivity_scores)
        best = max(productivity_scores)
        current_productivity = productivity_scores[-1]
        trend = self.calculate_trend(productivity_scores)
        score_trend = self.calculate_score_with_trend(current_productivity, trend)
        return {
            'avg': avg,
            'trend': trend,
            'best': best,
            'sessions': len(productivity_scores),
            'productivity': current_productivity,
            'score_trend': score_trend
        }
