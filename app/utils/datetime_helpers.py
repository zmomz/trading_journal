from sqlalchemy.orm import Session
from app.models.trade import Trade
from typing import List, Dict
from datetime import datetime, timedelta

def calculate_profit_loss(trades: List[Trade]):
    realized_profit = sum((trade.exit_price - trade.entry_price) * trade.position_size for trade in trades if trade.is_closed)
    unrealized_profit = sum((trade.exit_price - trade.entry_price) * trade.position_size for trade in trades if not trade.is_closed)
    return {"realized_profit": realized_profit, "unrealized_profit": unrealized_profit}

def calculate_win_loss_rate(trades: List[Trade]):
    wins = sum(1 for trade in trades if trade.is_closed and trade.exit_price > trade.entry_price)
    losses = sum(1 for trade in trades if trade.is_closed and trade.exit_price <= trade.entry_price)
    total = wins + losses
    return {"win_rate": (wins / total) * 100 if total > 0 else 0, "loss_rate": (losses / total) * 100 if total > 0 else 0}

def calculate_risk_reward_ratio(trades: List[Trade]):
    risk_reward_ratios = [(trade.take_profit - trade.entry_price) / (trade.entry_price - trade.stop_loss) for trade in trades if trade.stop_loss and trade.take_profit]
    avg_rrr = sum(risk_reward_ratios) / len(risk_reward_ratios) if risk_reward_ratios else 0
    return {"average_risk_reward_ratio": avg_rrr}

def calculate_annualized_return(trades: List[Trade]) -> Dict[str, float]:
    if not trades:
        return {"annualized_return": 0.0}
    start_date = min(trade.executed_at for trade in trades)
    end_date = max(trade.closed_at or datetime.utcnow() for trade in trades)
    days_held = (end_date - start_date).days or 1
    total_return = sum((trade.exit_price - trade.entry_price) * trade.position_size for trade in trades if trade.is_closed)
    annualized_return = (total_return / days_held) * 365 if days_held else 0
    return {"annualized_return": annualized_return}

def format_datetime(dt: datetime) -> str:
    return dt.strftime("%Y-%m-%d %H:%M:%S")

def get_time_difference(start: datetime, end: datetime = None) -> timedelta:
    end = end or datetime.utcnow()
    return end - start

def get_analytics_metrics(db: Session, user_id: int):
    trades = db.query(Trade).filter(Trade.user_id == user_id).all()
    return {
        **calculate_profit_loss(trades),
        **calculate_win_loss_rate(trades),
        **calculate_risk_reward_ratio(trades),
        **calculate_annualized_return(trades)
    }
