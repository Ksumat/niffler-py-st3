<html>
<head>
    <meta charset="UTF-8">
    <style>
        body {
            font-family: Arial, sans-serif;
            padding: 20px;
            background: #f5f5f5;
        }
        .status {
            font-size: 18px;
            font-weight: bold;
            padding: 10px;
            background: white;
            border-radius: 5px;
            margin-bottom: 15px;
        }
        .status-2xx { color: #155724; background: #d4edda; border: 1px solid #c3e6cb; }
        .status-4xx { color: #721c24; background: #f8d7da; border: 1px solid #f5c6cb; }
        .status-5xx { color: #856404; background: #fff3cd; border: 1px solid #ffeaa7; }
        .url {
            padding: 10px;
            background: #e9ecef;
            border-radius: 5px;
            margin-bottom: 15px;
            font-family: monospace;
            word-break: break-all;
        }
        pre {
            background: white;
            padding: 15px;
            border-radius: 5px;
            border: 1px solid #ddd;
            overflow-x: auto;
            font-family: 'Courier New', monospace;
            font-size: 14px;
        }
        table {
            width: 100%;
            border-collapse: collapse;
            background: white;
            border-radius: 5px;
            overflow: hidden;
        }
        th, td {
            padding: 8px 12px;
            border: 1px solid #ddd;
            text-align: left;
        }
        th {
            background: #f8f9fa;
            font-weight: bold;
            width: 30%;
        }
        h4 {
            margin-top: 20px;
            margin-bottom: 10px;
            color: #495057;
        }
    </style>
</head>
<body>
    <div class="status
        {% if response.status_code >= 200 and response.status_code < 300 %}status-2xx
        {% elif response.status_code >= 400 and response.status_code < 500 %}status-4xx
        {% elif response.status_code >= 500 %}status-5xx
        {% endif %}">
        Status code: {{ response.status_code }}
    </div>

    {% if response.url %}
    <div class="url">
        <strong>URL:</strong><br>{{ response.url }}
    </div>
    {% endif %}

    {% if response.body %}
    <h4>Body</h4>
    <pre>{{ response.body }}</pre>
    {% endif %}

    {% if response.headers %}
    <h4>Headers</h4>
    <table>
        <tbody>
            {% for name, value in response.headers.items() %}
            <tr>
                <th>{{ name }}</th>
                <td>{{ value or 'null' }}</td>
            </tr>
            {% endfor %}
        </tbody>
    </table>
    {% endif %}
</body>
</html>