from ..common import GetAction, ActionResponse, ActionRequest
from makolang.backends.moji import pronounce_x, pronounce
from makolang.backends.youdao import pronounce

def do(
    request: ActionRequest,
) -> ActionResponse:    
    backend = request.queries.get('backend', None)
    word = request.queries.get('word', None)
    lang = request.queries.get('lang', 'en')
    redirect = request.queries.get('redirect', False)
    if backend is None or word is None:
        return ActionResponse.fail(400, 'backend and word are required')
    
    backends = backend.split(',') if backend else ['moji', 'youdao']
    fail_messages = {}
    
    for backend in backends:
        try:
            if backend == 'moji':
                katakana = request.queries.get('katakana', '')
                allow_fallback = bool(request.queries.get('allow_fallback', False))
                result = pronounce_x(word, katakana, allow_fallback)
                if result is None:
                    raise Exception('No result')
            elif backend == 'youdao':
                result = pronounce(lang, word)
            else:
                return ActionResponse.fail(400, f'Unknown backend: {backend}')
            
            fail_messages[backend] = None
            if redirect:
                return ActionResponse.redirect(result.url)
            else:
                return ActionResponse.success({
                    'backend': backend,
                    'lang': lang,
                    'word': word,
                    'result': result,
                    'trials': fail_messages,
                })
        except Exception as e:
            fail_messages[backend] = str(e)
    
    return ActionResponse.fail(500, 'No backend succeeded', {'trials': fail_messages})
    # return ActionResponse.success({
    #     'pronounce': 1
    # })

__exports__ = [
    GetAction('/api/functions/word_pronounce', do)
]