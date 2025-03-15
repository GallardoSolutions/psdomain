from psdomain.services.media_content import MediaContentService

from .fixtures import HIT_RESPONSE, ARIEL_RESPONSE, SANMAR_RESPONSE


def test_media_content_service():
    srv = MediaContentService(HIT_RESPONSE)
    assert srv.highest_resolution == 0
    assert srv.get_blank_thumbnail_for_product('55410') == 'https://www.hitpromo.net/imageManager/show/55410_group.jpg'
    # Ariel
    srv = MediaContentService(ARIEL_RESPONSE)
    assert srv.highest_resolution == 1200
    assert len(srv.filter_by_product_id('ALB-AL23')) == 5
    assert len(srv.best_images) == 10
    prefix = 'https://d2b9vjwb3yw5iu.cloudfront.net/files'
    # it didn't pick the gif because it is alternate
    assert srv.get_blank_thumbnail_for_product('ALB-AL23') == f'{prefix}/Primary/blank/alb-al23.jpg'
    assert srv.get_blank_small_for_product('ALB-AL23') == f'{prefix}/Primary/blank/alb-al23.jpg'
    assert srv.get_blank_base_for_product('ALB-AL23') == f'{prefix}/Primary/blank/alb-al23.jpg'
    #
    assert len(srv.filter_by_product_id('ALB-AL23', True)) == 2
    #
    assert len(srv.filter_by_part_id('ALB-AL23NB')) == 5
    assert len(srv.filter_by_part_id('ALB-AL23NB', True)) == 2


def test_sanmar_vest_best_images():
    """
    NF0A3LH1
    :return:
    """
    srv = MediaContentService(SANMAR_RESPONSE)
    urls = {mc.url for mc in srv.best_images}
    assert len(urls) == 10
