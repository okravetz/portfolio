# Era milestone dates and sources

Checked 2026-10-30 for Phase 2 (the "time travel" eras). `docs/` is excluded from the Jekyll build, so this file is not published.

**How these were checked.** From web search results only. The pages marked "primary" are the originals; I could not open any of them from the build environment (w3.org and rfc-editor.org don't resolve there), so the dates below come from search-result summaries of those pages and from secondary sources. Re-check any date before it appears as site copy.

| Milestone | Date | Used for | Sources | Notes |
|---|---|---|---|---|
| First ARPANET host-to-host message (UCLA to SRI) | 29 October 1969, about 10:30 p.m. | 1969 | [Leonard Kleinrock, UCLA](https://www.lk.cs.ucla.edu/internet_first_words.html) (primary) | The message was meant to be "LOGIN"; the system crashed after "LO". |
| DEC VT100 introduced | August 1978 | 1983 | [Wikipedia: VT100](https://en.wikipedia.org/wiki/VT100); [Computer History Museum](https://www.computerhistory.org/revolution/input-output/14/349/1697) | The museum gives 1978 only. The month is from Wikipedia. |
| ARPANET moves from NCP to TCP/IP | 1 January 1983 | 1983 | [RFC 801, NCP/TCP transition plan (Nov 1981)](https://www.rfc-editor.org/info/rfc801/) (primary); [Vint Cerf, Internet History list, 2009](https://elists.isoc.org/pipermail/internet-history/2009-April/000793.html); [Wikipedia: Network Control Protocol](https://en.wikipedia.org/wiki/Network_Control_Protocol_(ARPANET)) | See "Differences from the plan". |
| "HTML Tags" document, the first public description of HTML | Late 1991 | 1991 | [Web Design Museum](https://www.webdesignmuseum.org/web-design-history/tim-berners-lee-published-a-document-called-html-tags-1991); Wikipedia's HTML article (via mirrors) | See "Differences from the plan". |
| NCSA Mosaic 1.0 (X Window System) | Announced 21 April 1993; release dated 22 April 1993 | 1996 context | [Wikipedia: NCSA Mosaic](https://en.wikipedia.org/wiki/NCSA_Mosaic); [www-talk announcement](https://ksi.cpsc.ucalgary.ca/archives/WWW-TALK/www-talk-1993q2.messages/126.html) (primary) | Windows and Mac ports came later in 1993. |
| Netscape Navigator 3.0 final release | 17 to 19 August 1996 | 1996 | [TidBITS, 19 Aug 1996](https://tidbits.com/1996/08/19/netscape-3-0-ships/) ("shipped today"); [PC Watch](https://pc.watch.impress.co.jp/docs/article/960819/ns30.htm) (17 Aug, Pacific time) | Sources differ by two days. Internet Explorer 3.0 shipped 13 August 1996 ([Wikipedia](https://en.wikipedia.org/wiki/Internet_Explorer_3)). |
| Adobe announces Flash Player end of life | 25 July 2017 | 2001 | [Adobe blog, "Flash & the Future of Interactive Content"](https://blog.adobe.com/en/publish/2017/07/25/adobe-flash-update) (primary) | Adobe said it would stop updating and distributing Flash Player at the end of 2020. |
| Flash Player end of life | 31 December 2020 | 2001 | [Adobe, Flash Player End of Life](https://www.adobe.com/products/flashplayer/end-of-life-alternative.html) (primary) | Adobe began blocking Flash content from running on 12 January 2021. |
| First Web 2.0 Conference | 5 to 7 October 2004, San Francisco | 2006 | [Wikipedia: Web 2.0 Summit](https://en.wikipedia.org/wiki/Web_2.0_Summit); [John Battelle's announcement, May 2004](https://battellemedia.com/archives/2004/05/web_20_the_conference/amp) | O'Reilly and MediaLive. The venue (Hotel Nikko) is from one summary; I did not confirm it. |
| "Responsive Web Design" by Ethan Marcotte, A List Apart | 25 May 2010 | 2013 | [Jeffrey Zeldman, 25 May 2010](https://zeldman.com/2010/05/25/responsive-web-design); [Web Design Museum](https://www.webdesignmuseum.org/web-design-history/responsive-web-design-2010) | I did not open the A List Apart article itself. |
| iOS 7 announced, then released | Announced 10 June 2013 (WWDC); released 18 September 2013 | 2013 | [Carleton University IT, "iOS 7 released"](https://carleton.ca/mobileservices/2013/ios-7-released/); [AppleInsider forum thread, Sept 2013](https://forums.appleinsider.com/discussion/159447); Wikipedia mirrors | Weakest sourcing of the list: no Apple page was reached. |

## Differences from the plan

The plan's dates held up. Two need different wording:

1. **"The TCP/IP switch on 1 Jan 1983."** RFC 801 set 1 January 1983 as the *goal* for the switch. Sources agree it was the official cutoff, but some sites kept using NCP into mid-1983 with permission, and Vint Cerf called the date "a deadline, which, of course, was not met" in full. Safe wording: "the ARPANET's official switch to TCP/IP, 1 January 1983".
2. **"HTML Tags (Oct 1991)."** The sources say "late 1991". One entry (Web Design Museum) is reported to give a specific October date, but I could not confirm the day or month from the original. Use "1991" unless Oren has the original message.

## Open checks before PR 3

- **The "18 tags".** Sources say the document described 18 elements. The tag list a secondary source gives (title, nextid, a, isindex, plaintext, listing, p, h1 to h6, address, hp1, hp2, dl, dt, dd, ul, li, menu, dir) has more names than that if h1 to h6 are counted one by one, so how the 18 is counted is unclear. The 1991 layout's allowed-tag list should be checked against the original document, not this table.
- **Not on the plan's list, so not sourced:** the Bootstrap 3 release date (the 2013 era is "Bootstrap-3-style") and the 1996 hit counter's year. Nothing on the site depends on them yet.
