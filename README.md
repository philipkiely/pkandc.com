# pkandc.com

This repository contains the static site generator and source files that power my Philip Kiely & Company's website, [https://pkandc.com](https://pkandc.com).

The code for this site is open-source under the MIT license, but the content (page copy, original images, etc) is copyright Philip Kiely & Company, please don't reproduce that part.

### Initial Setup

Requires Python 3.7+ and Node.js 14+.

Run the following:

```
git clone git@github.com:philipkiely/pkandc.com.git
cd pkandc.com
mkvirtualenv pkandc.com
pip install -r requirements.txt
npm i
```

### Development

To work on the project:

```
cd ~/Code/pkandc.com
workon pkandc.com
python build.py --dev
```

### Deployment

This site runs on Netlify and is deployed from the `main` branch.

### TODO

[ ] homepage
[ ] editorial page
[ ] about
[ ] contact
[ ] build.py - mkdocs (or maybe subdomain/separate repo)
[ ] document

Subdomains:

* docs: mkdocs

Email - Hey for Work - first@pkandc.com

Maybe the architecture is by subdomain, each with its own dist

/index
/docs
/app
/api
/status
/assets

Eh maybe not subdomains for SEO purposes, I want all of the keyword-heavy content in docs especially to attribute to the same place.