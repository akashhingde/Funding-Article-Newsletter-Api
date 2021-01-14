# Funding Article Newsletter API
This Api Fetch the articles related funding news.

## Installation
Use the package manager pip to install all requirements libraries which we want for run the program.

```bash
pip3 install -r requirements.txt
```

## How To Run Server Program File
To perform following command

Step 1:-
```bash
python3 app.py
```
Step 2:-
Open the browser and hit this url http://0.0.0.0:5000/getnews

## Output
1.ok response
```python
{
    status:SUCCESS,
    data:[
        #all the news articles
    ]
}
```
2.error response
```python
    status:ERROR,
    data:[
        #null
    ]
}
```
