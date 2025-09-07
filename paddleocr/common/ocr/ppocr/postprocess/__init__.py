from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import copy

__all__ = ['build_post_process']

from .db_postprocess import DBPostProcess, DistillationDBPostProcess
from .rec_postprocess import CTCLabelDecode, AttnLabelDecode, SRNLabelDecode, \
    DistillationCTCLabelDecode, NRTRLabelDecode, SARLabelDecode, \
    SEEDLabelDecode, PRENLabelDecode, ViTSTRLabelDecode, ABINetLabelDecode, \
    SPINLabelDecode, VLLabelDecode, RFLLabelDecode
from .cls_postprocess import ClsPostProcess
from .vqa_token_ser_layoutlm_postprocess import VQASerTokenLayoutLMPostProcess, DistillationSerPostProcess
from .vqa_token_re_layoutlm_postprocess import VQAReTokenLayoutLMPostProcess, DistillationRePostProcess


def build_post_process(config, global_config=None):
    support_dict = [
        'DBPostProcess',
        'CTCLabelDecode', 
        'ClsPostProcess',
        'VQASerTokenLayoutLMPostProcess',
        'VQAReTokenLayoutLMPostProcess', 
        'DistillationSARLabelDecode',
        'DistillationSerPostProcess',
    ]

    if config['name'] == 'PSEPostProcess':
        from .pse_postprocess import PSEPostProcess
        support_dict.append('PSEPostProcess')

    config = copy.deepcopy(config)
    module_name = config.pop('name')
    if module_name == "None":
        return
    if global_config is not None:
        config.update(global_config)
    assert module_name in support_dict, Exception(
        'post process only support {}'.format(support_dict))
    module_class = eval(module_name)(**config)
    return module_class
