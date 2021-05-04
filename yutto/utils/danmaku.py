import os
from typing import Literal, Optional, TypedDict, Union

from biliass import Danmaku2ASS

DanmakuSourceType = Literal["xml", "protobuf", "no"]
DanmakuSaveType = Literal["xml", "ass", "no"]

DanmakuSourceDataXml = str
DanmakuSourceDataProtobuf = bytes
DanmakuSourceDataType = Union[DanmakuSourceDataXml, DanmakuSourceDataProtobuf]


class DanmakuData(TypedDict):
    source_type: DanmakuSourceType
    save_type: DanmakuSaveType
    data: Optional[DanmakuSourceDataType]


def write_xml_danmaku(xml_danmaku: str, filepath: str):
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(xml_danmaku)


def write_ass_danmaku(xml_danmaku: str, filepath: str, height: int, width: int):
    with open(
        filepath,
        "w",
        encoding="utf-8-sig",
        errors="replace",
    ) as f:
        f.write(
            Danmaku2ASS(
                xml_danmaku,
                width,
                height,
                reserve_blank=0,
                font_face="sans-serif",
                font_size=width / 40,
                text_opacity=0.8,
                duration_marquee=15.0,
                duration_still=10.0,
                comment_filter=None,
                is_reduce_comments=False,
                progress_callback=None,
            )
        )


def write_danmaku(danmaku: DanmakuData, video_path: str, height: int, width: int) -> Optional[str]:
    video_path_no_ext = os.path.splitext(video_path)[0]
    if danmaku["source_type"] == "xml":
        if danmaku["save_type"] == "xml":
            file_path = video_path_no_ext + ".xml"
            xml_danmaku = danmaku["data"]
            assert isinstance(xml_danmaku, str)
            write_xml_danmaku(xml_danmaku, file_path)
        elif danmaku["save_type"] == "ass":
            file_path = video_path_no_ext + ".ass"
            xml_danmaku = danmaku["data"]
            assert isinstance(xml_danmaku, str)
            write_ass_danmaku(xml_danmaku, file_path, height, width)
        else:
            return None
    else:
        return None
