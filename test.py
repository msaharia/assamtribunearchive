import grequests as async
# If using requests > v0.13.0, use
# from grequests import async

urls = [
    'http://python-requests.org',
    'http://httpbin.org',
    'http://python-guide.org',
    'http://kennethreitz.com'
]

urls2 = []

# A simple task to do to each response object
def do_something(response):
    urls2.append = print(response.url)

# A list to hold our things to do via async
async_list = []

for u in urls:
    # The "hooks = {..." part is where you define what you want to do
    # 
    # Note the lack of parentheses following do_something, this is
    # because the response will be used as the first argument automatically
    action_item = async.get(u, hooks = {'response' : do_something})

    # Add the task to our list of things to do via async
    async_list.append(action_item)

# Do our list of things to do via async
async.map(async_list)
