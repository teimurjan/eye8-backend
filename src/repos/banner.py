from src.storage.base import Storage
from src.models import Banner, BannerText, BannerLinkText
from src.repos.base import Repo, with_session, set_intl_texts


class BannerRepo(Repo):
    def __init__(self, db_conn, file_storage: Storage):
        super().__init__(db_conn, Banner)
        self.__file_storage = file_storage

    @with_session
    def add_banner(
        self,
        texts,
        link_texts,
        link,
        image,
        text_color,
        text_top_offset,
        text_left_offset,
        text_right_offset,
        text_bottom_offset,
        session
    ):
        banner = Banner()

        set_intl_texts(texts, banner, 'texts', BannerText, session=session)
        set_intl_texts(link_texts, banner, 'link_texts',
                       BannerLinkText, session=session)

        banner.link = link
        banner.text_color = text_color
        banner.text_top_offset = text_top_offset
        banner.text_left_offset = text_left_offset
        banner.text_right_offset = text_right_offset
        banner.text_bottom_offset = text_bottom_offset

        banner.image = self.__file_storage.save_file(image)

        session.add(banner)
        session.flush()

        banner.link_texts
        banner.created_on
        banner.updated_on

        return banner

    @with_session
    def update_banner(
        self,
        id_,
        texts,
        link_texts,
        link,
        image,
        text_color,
        text_top_offset,
        text_left_offset,
        text_right_offset,
        text_bottom_offset,
        session
    ):
        banner = self.get_by_id(id_, session=session)

        set_intl_texts(texts, banner, 'texts', BannerText, session=session)
        set_intl_texts(link_texts, banner, 'link_texts',
                       BannerLinkText, session=session)

        banner.link = link
        banner.text_color = text_color
        banner.text_top_offset = text_top_offset
        banner.text_left_offset = text_left_offset
        banner.text_right_offset = text_right_offset
        banner.text_bottom_offset = text_bottom_offset

        if image is not None:
            banner.image = (image
                            if isinstance(image, str)
                            else self.__file_storage.save_file(image))

        session.flush()

        banner.created_on
        banner.updated_on

        return banner

    class DoesNotExist(Exception):
        pass
