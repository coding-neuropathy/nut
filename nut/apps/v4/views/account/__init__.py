from apps.core.utils.http import SuccessJsonResponse, ErrorJsonResponse
from apps.core.forms.account import UserPasswordResetForm
from apps.mobile.forms.account import MobileUserSignInForm, MobileUserSignUpForm, MobileUserSignOutForm
from apps.mobile.lib.sign import check_sign

# from apps.mobile.models import Session_Key

from django.views.decorators.csrf import csrf_exempt
from django.utils.log import getLogger


log = getLogger('django')



@csrf_exempt
@check_sign
def login(request):
    if request.method == "POST":
        _forms = MobileUserSignInForm(request=request, data=request.POST)
        log.info(request.POST)
        if _forms.is_valid():
            _forms.login()
            _user = _forms.get_user()

            res = {
                'user': _user.v3_toDict(),
                'session': _forms.get_session()
            }
            return SuccessJsonResponse(res)
    else:
        _forms = MobileUserSignInForm(request=request)

    # dict(_forms.errors))
    for k, v in dict(_forms.errors).items():
        return ErrorJsonResponse(status=400, data={
            'type': k,
            'message': v,
        })

    return ErrorJsonResponse(status=400)


@csrf_exempt
@check_sign
def register(request):
    if request.method == "POST":
        _forms = MobileUserSignUpForm(request=request, data=request.POST, files=request.FILES)
        log.info(request.FILES)
        if _forms.is_valid():
            _user = _forms.save()
            log.info("user user %s" % _user.v3_toDict())
            res = {
                'user':_user.v3_toDict(),
                'session': _forms.get_session()
            }
            return SuccessJsonResponse(res)
        for k, v in dict(_forms.errors).items():
            log.info(v.as_text().split('*'))
            error_msg = v.as_text().split('*')[1]
            return ErrorJsonResponse(status=409, data={
                'type': k,
                'message': error_msg.lstrip(),
            })

    return ErrorJsonResponse(status=400)


@csrf_exempt
@check_sign
def forget_password(request):
    # if request.method == "POST":
    if request.method == 'POST':
        _forms = UserPasswordResetForm(request.POST)
        if _forms.is_valid():
            _forms.save(domain_override='guoku.com',
                        subject_template_name='web/mail/forget_password_subject.txt',
                        email_template_name='web/mail/forget_password.html',
                        from_email='hi@guoku.com')
            return SuccessJsonResponse(data={ 'success' : '1' })
        return ErrorJsonResponse(
                data = {
                    'type' : 'email',
                    'message' : 'email does not exist',
                },
                status = 400
            )
    return ErrorJsonResponse(status=400)


@csrf_exempt
@check_sign
def logout(request):
    # _req_uri = request.get_full_path()
    if request.method == "POST":
        _forms = MobileUserSignOutForm(request.POST)
        if _forms.is_valid():
            res = _forms.logout()
            return SuccessJsonResponse({ 'success': '1' })

    return ErrorJsonResponse(status=400)




@csrf_exempt
@check_sign
def apns_token(request):

    log.info(request.POST)
    return SuccessJsonResponse()

__author__ = 'edison'
