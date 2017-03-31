from ir.nodes import *
from frame.frame import Frame


def reorder_blocks(seq, frame):
    """Reorder blocks in seq so that the negative branch of a CJUMP always
    follows the CJUMP itself. frame is the frame of the corresponding
    function."""
    assert(isinstance(seq, SEQ))
    assert(isinstance(frame, Frame))
    blocks = {}
    inside_block = False
    for stm in seq.stms:
        if isinstance(stm,LABEL):
            if inside_block:
                blocks[current_label] = JUMP(NAME(stm.label.name))
            current_label = stm.label.name
            blocks[current_label] = []
            inside_block = True
        elif inside_block:
            if isinstance(stm,CJUMP) or isinstance(stm,JUMP):
                blocks[current_label].append(stm)
                inside_block = False
            elif not isinstance(stm,LABEL):
                blocks[current_label].append(stm)
    print(blocks)
    return seq
