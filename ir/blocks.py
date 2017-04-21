from ir.nodes import *
from frame.frame import Frame


def reorder_blocks(seq, frame):
    """Reorder blocks in seq so that the negative branch of a CJUMP always
    follows the CJUMP itself. frame is the frame of the corresponding
    function."""
    # Sorting blocks
    assert(isinstance(seq, SEQ))
    assert(isinstance(frame, Frame))
    blocks = []
    inside_block = False
    index = 0
    for stm in seq.stms:
        if isinstance(stm,LABEL):
            if inside_block:
                blocks[index] += JUMP(NAME(stm.label))
            current_label = stm.label.name
            blocks[index] = [current_label]
            inside_block = True
        elif inside_block:
            if isinstance(stm,CJUMP) or isinstance(stm,JUMP):
                blocks[index] += stm
                inside_block = False
                index += 1
            elif not isinstance(stm,LABEL):
                blocks[index] += stm
    print(blocks)
    # Trace determination
    blocks_examined = {}'''
    blocks = {}
    labels = []
    inside_blocks = False
    for stm in seq.stms:
        if isinstance(stm,LABEL):
            if inside_blocks:
                next_label = stm.label.name
                blocks[current_label].append(JUMP(NAME(next_label)))
            current_label = stm.label.name
            labels.append(current_label)
            blocks[current_label] = []
            inside_blocks = True
        elif inside_blocks:
            if not isinstance(stm,LABEL):
                blocks[current_label].append(stm)
            if isinstance(stm,JUMP) or isinstance(stm,CJUMP):
                inside_blocks = False
    print(blocks)
    print(labels)'''
    return seq
