from jinja2 import Template

HTML_TEMPLATE = """
<html>
<head><title>Investment Report</title></head>
<body>
<h1>{{ company }}</h1>

<p><b>Signal:</b> {{ signal }}</p>
<p><b>Confidence:</b> {{ confidence }}</p>

<h2>Thesis</h2>
<p>{{ thesis }}</p>

<h2>Insights</h2>
<ul>
{% for i in insights %}
<li>{{ i }}</li>
{% endfor %}
</ul>

<h2>Risks</h2>
<ul>
{% for r in risks %}
<li>{{ r }}</li>
{% endfor %}
</ul>

</body>
</html>
"""

def generate_html_report(data: dict) -> str:
    template = Template(HTML_TEMPLATE)
    return template.render(**data)