# Placeholder for DJ agent playlist ordering

from metadata import get_metadata

def order_playlist(tracks, blocks, rules):
    """
    Order tracks according to block schedule and avoid repeated artists within a block if possible.
    tracks: list of dicts with at least 'query' (YouTube title or search string)
    blocks: list of dicts with 'name', 'duration', 'instructions'
    rules: dict of advanced rules
    Returns: ordered list of tracks (with metadata)
    """
    # Gather metadata for each track
    track_infos = []
    for t in tracks:
        meta = get_metadata(t.get('query', ''))
        track_infos.append({**t, **meta})

    # Simple ordering: assign tracks to blocks in order, cycling if needed
    ordered = []
    block_idx = 0
    for i, track in enumerate(track_infos):
        block = blocks[block_idx]
        track['block'] = block['name']
        ordered.append(track)
        block_idx = (block_idx + 1) % len(blocks)
    return ordered 