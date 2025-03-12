import os

from h26x_extractor.h26x_parser import H26xParser
from uuid import uuid4

SLICE_TYPES = {0: 'P', 1: 'B', 2: 'I', 3: 'SP', 4: 'SI'}
FLAG_VIDEO = 'flag.mp4'
ORIGIN_H264='encode-origin.h264'
OUTPUT_H264='encode-new.h264'
OUTPUT_MP4='encode-output.mp4'
OUTPUT_FLV='encode-output.flv'
class BitStream:
    def __init__(self, buf):
        self.buffer = buf
        self.bit_pos = 0
        self.byte_pos = 0

    def ue(self):
        count = 0
        while self.u(1) == 0:
            count += 1
        res = ((1 << count) | self.u(count)) - 1
        return res

    def u1(self):
        self.bit_pos += 1
        res = self.buffer[self.byte_pos] >> (8 - self.bit_pos) & 0x01
        if self.bit_pos == 8:
            self.byte_pos += 1
            self.bit_pos = 0
        return res

    def u(self, n: int):
        res = 0
        for i in range(n):
            res <<= 1
            res |= self.u1()
        return res


def extract_slice_type(nalu_body):
    body = BitStream(nalu_body)
    #print(nalu_body[:3])
    first_mb_in_slice = body.ue()
    slice_type = body.ue()
    return slice_type


def generate_sequence_data(origin_slice_type_list: list):
    sei_data = b'\x00\x00\x01\x06\x05'
    sei_payload_len = len(origin_slice_type_list) + 16
    uuid = uuid4().bytes
    while sei_payload_len > 255:
        sei_payload_len -= 255
        sei_data += b'\xFF'
    sei_payload = uuid + ''.join(origin_slice_type_list).encode()
    sei_data += int.to_bytes(sei_payload_len, 1, 'big')
    sei_data += sei_payload
    sei_data += b'\x80'
    return sei_data


if __name__ == '__main__':
    os.system(f'ffmpeg -i {FLAG_VIDEO} -c:v libx264 -crf 18 -preset medium -c:a aac -b:a 128k {ORIGIN_H264}')
    f = open(ORIGIN_H264, 'rb')
    origin_data = list(f.read())
    f.close()
    # 进行加密
    H26xParser = H26xParser(ORIGIN_H264, verbose=False)
    H26xParser.parse()
    nalu_list = H26xParser.nalu_pos
    print(nalu_list)
    data = H26xParser.byte_stream
    origin_slice_type_list = []
    sei_data_list = []
    for tu in nalu_list:
        start, end, _, _, _, _ = tu
        rbsp = bytes(H26xParser.getRSBP(start, end))
        nalu_header = rbsp[0]
        nal_unit_type = nalu_header & 0x1F
        nalu_body = rbsp[1:]
        if nal_unit_type == 1:  #修改slice
            slice_type = extract_slice_type(nalu_body)
            origin_slice_type_list.append(SLICE_TYPES[slice_type % 5])
            print(SLICE_TYPES[slice_type % 5], end=' ')
            origin_data[start + 1] = origin_data[start + 1] | 0x4  # 非关键帧全部变为B帧
        elif nal_unit_type == 5:
            origin_data[start + 1] = origin_data[start + 1] | 0x4  # 把关键帧slice_type改为11
        elif nal_unit_type == 7 and origin_slice_type_list:
            sei_data_list.append(generate_sequence_data(origin_slice_type_list))
            origin_slice_type_list = []
    sei_data_list.append(generate_sequence_data(origin_slice_type_list))
    # 构造新数据
    origin_slice_type_list = []
    new_data = b''
    start_pos = 0
    count = 0
    for start, end, _, _, _, _ in nalu_list:
        rbsp = bytes(H26xParser.getRSBP(start, end))
        nalu_header = rbsp[0]
        nal_unit_type = nalu_header & 0x1F
        if nal_unit_type == 5:
            new_data += bytes(origin_data[start_pos:end]) + sei_data_list[count]
            count += 1
            start_pos = end
    new_data += bytes(origin_data[start_pos:])
    # 输出
    f = open(OUTPUT_H264, 'wb')
    f.write(bytes(new_data))
    f.close()
    # 封装
    os.system(f"ffmpeg -i {OUTPUT_H264} -vcodec copy {OUTPUT_MP4}")
    os.system(f"ffmpeg -i {OUTPUT_MP4} -vcodec copy {OUTPUT_FLV}")
