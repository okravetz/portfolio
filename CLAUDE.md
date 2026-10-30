# orenkravetz.com

Oren Kravetz's portfolio site. Jekyll, deployed to GitHub Pages at www.orenkravetz.com.

## How the site is built

- **Deploys:** every push to `main` builds and publishes the live site (`.github/workflows/jekyll.yml`). There is no staging environment.
- **Homepage:** `index.html` (About with the clients card, Work, Résumé, Contact). Nav labels come from `_data/navigation.yml`. "More work" rows are in `_data/morework.yml` (first 3 show, the rest sit behind a toggle).
- **Case studies:** homepage cards live in `_data/casestudies.yml` (`publish: false` hides a card; a card with no `link` isn't clickable). The three current studies are `casestudies/amex-value-builder.md`, `imax-relaunch.md` and `lhw-travel-advisor-portal.md`. Their text, facts and figures are in the front matter, and `_layouts/casestudy.html` renders them (a page with `overview:` in its front matter uses the new template; `01.md`–`05.md` are the old studies, hidden from the homepage, and use the old template in the same layout). Images are in `assets/images/wf/`.
- **Contact:** `_includes/contact.html` and `_data/contact.yml`.
- **Résumé download:** `assets/files/Resume 2026.pdf`, with a preview image at `assets/images/Resume 2026.png`. Update both together.
- **Analytics:** Google Analytics 4 (`G-167RBEBRWP`), base tag only, in `_layouts/default.html`, `_layouts/casestudy.html` and `_includes/ga4.html` (the era pages). Change it in all three. The time-travel bar sends `time_travel` (`from_era`, `to_era`) and, on Today, `time_travel_open` (`opened_from`: `footer` (the floating Time travel button, bottom right) or `about_ps`).
- **Time-travel eras:** each era homepage is `eras/<year>.html` (front matter only: layout, `era`, `permalink`) rendered by `_layouts/era-<year>.html`. The eras, their order and which are live (`ready: true`) are in `_data/eras.yml`; the bar is `_includes/time-travel.html` with `_sass/_time-travel.scss` and `assets/js/time-travel.js`. Era pages load `assets/css/era.css` (plus their own, e.g. `era-1969.css`), never the main stylesheet. 1969 and 1983 are text only: their copy is built by `_includes/era-text/` (ASCII swaps in Liquid, capitals for 1969), and 1983's menu buttons and keyboard use `assets/js/bbs.js`. On the Future page the question chips stay docked above the time-travel bar while reading. 2001's intro (once per browser tab, `sessionStorage` key `intro-2001`), rollovers and section switching are `assets/js/era-2001.js`; 2013's phone menu button is `assets/js/era-2013.js`. 2006's tag cloud sizes are counted from `morework.yml` plus the published case studies. The Future page (`eras/future.html`) answers six scripted questions (`_data/future.yml`) with text pulled from `_data/`, and shows the page's own JSON-LD under "What an agent sees"; that Person JSON-LD is `_includes/jsonld.html`, built from `site.yml`, `contact.yml` and the published case studies, and is also in the `<head>` of Today. On Today the bar stays open once a visitor has opened it or used it to leave, until they close it (`sessionStorage` key `tt-open`); Close just closes it (the page stays where it is), and the button that opens it floats at the bottom right (hidden while the bar is open). Images with text in them come from `scripts/era-assets.py` (see `docs/era-assets.md`). The all-work pages (`/1969/work/` to `/2006/work/`, every row of `morework.yml`) are `eras/<year>-work.html` (front matter plus `work: true`), drawn by the same era layout; "Show all work" links to them (1969 has no links in its text: a row of keycaps below the paper, listed in `eras.yml` under `ui.keys`, opens the résumé, portfolio, all work, email and LinkedIn, and its work page gets a Back key; 1983 draws its links as `[letter]` commands (`_includes/era-text/cmd.html`, letters in `ui.commands`, contact letters from each label), and `bbs.js` lets visitors type a menu or command letter or use the arrow keys while the terminal has focus), and 2013 and Today expand the list in place instead. `/1992/` redirects to `/1991/` (`jekyll-redirect-from`).
- **Era accessibility:** every era page has one `<h1>`, landmarks (`main`, plus `nav` where there is one) and visible focus. The landmarks are invisible: ARIA roles on the period markup (`<center role="main">` on 1996 and 2001), or HTML5 elements that carry no styling. 1969's HTML keeps the copy's own capitalisation and CSS draws the capitals, so screen readers read "PMs", not "PMS"; its `@TYPE` lines are headings. 1983's name box is hidden from screen readers behind a hidden `<h1>`, its section titles are headings, and a hidden live region announces a section when the menu switches to it. The cursor blinks five times after each command, then stays lit. The 1996 marquee pauses on hover and keyboard focus and stays still with reduced motion. `era.css` keeps anything reached with Tab clear of the time-travel bar (`scroll-padding-bottom`). The 2006 green button is generated darker so its white text passes 4.5:1. Check with axe-core and a keyboard walk before changing an era.
- **Clients logos:** one-color logos in `assets/images/logos/`, listed in `_data/clients.yml`. The Home Depot is under NDA and must never appear.
- **Legacy pages:** the old accessibility statement and audit reports were removed. The old `1991/`, `1992/`, and `archive/` folders are still excluded from the build (in `_config.yml`); the new era pages live in `eras/`. `assets/incoming/` (originals for the redesign) is also excluded, so it isn't served. `_site/` is committed build output; don't edit it by hand.
- **Local preview:** `bundle install`, then `bundle exec jekyll serve`.

## Workflow

- Work on a branch and open a pull request for Oren to review. Don't push to `main` unless Oren says to for that change.
- Keep commits small and say in the description what changed on the live site.
- Check a change renders (local build or a careful read of the Liquid) before opening the PR.

## Content rules (from Oren's job-search project)

The site is part of a job search for UX Director / UX Manager roles. Its claims have to match the résumé and PDF portfolio.

1. **Never invent or inflate.** No made-up metrics, team sizes, titles, dates, outcomes, or client results. If a detail is missing, ask Oren.
2. **Attribute results** to whoever produced them. Client- or firm-level results are worded as such ("Santander reported…", "the team secured…").
3. **Scope:** Oren leads project teams of 1–5. Don't write language that implies larger leadership scope.
4. **Voice:** Oren drafts, Claude edits. Make minimal edits to his wording and give a short reason for each. Plain and specific; no buzzwords ("orchestration," "spearheaded," "proven track record," "passionate about").
5. **Say what you can't verify** instead of guessing.

## Sources of truth

- **Résumé:** the "Resume 2026" Google Doc, tab "Latest". Titles and dates follow LinkedIn.
- **Accuracy log:** `claude/consistency-log.md` in Oren's claude.ai "Job Search" project. Read it before changing any claim; it records which figures and wordings are correct. If you can't reach it, ask Oren.
- Facts that have gone wrong before:
  - Openbank: more than **$6B** (billion, not million) in deposits in its first U.S. year, as reported by Santander.
  - The agentic-AI A/B-testing prototype's client stays **unnamed** everywhere.
