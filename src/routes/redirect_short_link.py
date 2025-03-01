from flask import redirect, render_template, request
from flaskr.app import app
from flaskr.services.link_services import link_by_alias
from flaskr.services.link_services import update


@app.route('/<string:alias>', methods=['GET'])
def redirect_short_link(alias):
    link = link_by_alias(alias)
    if link is None:
        return redirect('/')

    if link.is_phishing is False:
        link.click_times += 1
        update(link)
        if link.password is None:
            return redirect(link.url)

        return render_template('redirect_shorten_link.html', link_id=link.id)

    previous_url = request.referrer
    if previous_url is None:
        return render_template('redirect_shorten_link.html', link_id=None, url='/',
                               error_message="This url has been blocked by our systems as potentially harmful")

    return render_template('redirect_shorten_link.html', link_id=None, url=previous_url,
                           error_message="This url has been blocked by our systems as potentially harmful")
