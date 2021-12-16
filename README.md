# The-Pile-FreeLaw

Download, parse, and filter data from [Court Listener](https://www.courtlistener.com/api/bulk-info/), part of the FreeLaw project. Data-ready for [The-Pile](https://github.com/EleutherAI/The-Pile).

While Data exists for multiple modalites (eg. dockets, people, ...), we focus on court opinions for language modeling.

### Pile-V2 Statistics

    ✔ Saved to data/FreeLaw_Opinions.jsonl.zst
    ℹ Date completed 12/15/2021
    ℹ Saved 4,940,710 opinions (1,378,695 added, 38.7% growth)
    ℹ Uncompressed filesize 69,470,526,055
    ℹ Compressed filesize   20,975,955,178
    ℹ sha256sum 8a38c34f181aa121c3a7360ad63e3e8c0b1ea0913de08a4bf1b68b3eabae3e66

Additional columns to find free text were added [`html_columbia`,
`html_anon_2020`, `html_with_citations`, `xml_harvard`] which accounts
for the larger increase from V1 to V2.

### Pile-V1 Statistics

    ✔ Saved to data/FreeLaw_Opinions.jsonl.zst
    ℹ Saved 3,562,015 opinions
    ℹ Uncompressed filesize   56,138,746,490
    ℹ Compressed filesize     17,013,175,549
    ℹ sha256sum 7d7ba907cf397e8585bb3ef148b3e9678edbf142b2247460f907c16aecbaed2d