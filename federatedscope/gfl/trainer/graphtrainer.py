from federatedscope.register import register_trainer
from federatedscope.core.trainers.trainer import GeneralTorchTrainer
from federatedscope.core.trainers.context import CtxReferVar


class GraphMiniBatchTrainer(GeneralTorchTrainer):
    def _hook_on_batch_forward(self, ctx):
        batch = ctx.data_batch.to(ctx.device)
        pred = ctx.model(batch)
        label = batch.y.squeeze(-1).long()
        if len(label.size()) == 0:
            label = label.unsqueeze(0)
        ctx.loss_batch = ctx.criterion(pred, label)

        ctx.batch_size = len(label)
        ctx.var.y_true = CtxReferVar(label, "batch")
        ctx.var.y_prob = CtxReferVar(pred, "batch")


def call_graph_level_trainer(trainer_type):
    if trainer_type == 'graphminibatch_trainer':
        trainer_builder = GraphMiniBatchTrainer
        return trainer_builder


register_trainer('graphminibatch_trainer', call_graph_level_trainer)