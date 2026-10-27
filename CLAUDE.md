# orenkravetz.com

Oren Kravetz's portfolio site. Jekyll, deployed to GitHub Pages at www.orenkravetz.com.

## How the site is built

- **Deploys:** every push to `main` builds and publishes the live site (`.github/workflows/jekyll.yml`). There is no staging environment.
- **Homepage:** `index.html` (About, Résumé, Clients, Work, Contact). Nav labels come from `_data/navigation.yml`.
- **Case studies:** cards and image lists live in `_data/casestudies.yml` (`publish: false` hides a card). Page text lives in `casestudies/01.md`–`05.md` and uses `_layouts/casestudy.html`. Images are in `assets/images/wf/`.
- **Contact:** `_includes/contact.html` and `_data/contact.yml`.
- **Résumé download:** `assets/files/Resume 2026.pdf`, with a preview image at `assets/images/Resume 2026.png`. Update both together.
- **Analytics:** Google Analytics 4 (`G-167RBEBRWP`), base tag only, in both layouts (`_layouts/default.html`, `_layouts/casestudy.html`). Change it in both places.
- **Clients logos:** an Elfsight widget, configured on Elfsight's site, not in this repo.
- **Legacy pages:** `1991/`, `1992/`, `archive/`, and `accessibility/` are old pages that still publish. `_site/` is committed build output; don't edit it by hand.
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
