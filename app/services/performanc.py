from sqlalchemy.orm import Session
from app.models.trade import Trade
from typing import List

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

def get_performance_metrics(db: Session, user_id: int):
    trades = db.query(Trade).filter(Trade.user_id == user_id).all()
    return {
        **calculate_profit_loss(trades),
        **calculate_win_loss_rate(trades),
        **calculate_risk_reward_ratio(trades)
    }
