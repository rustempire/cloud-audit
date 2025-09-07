__all__ = ["build_backbone"]


def build_backbone(config, model_type):
    if model_type == 'vqa':
        from .kie_unet_sdmgr import Kie_backbone
        from .vqa_layoutlm import LayoutLMForSer, LayoutLMv2ForSer, LayoutLMv2ForRe, LayoutXLMForSer, LayoutXLMForRe
        support_dict = [
            'Kie_backbone', 'LayoutLMForSer', 'LayoutLMv2ForSer',
            'LayoutLMv2ForRe', 'LayoutXLMForSer', 'LayoutXLMForRe'
        ]
    else:
        raise NotImplementedError

    module_name = config.pop('name')
    assert module_name in support_dict, Exception(
        "when model typs is {}, backbone only support {}".format(model_type,
                                                                 support_dict))
    module_class = eval(module_name)(**config)
    return module_class
