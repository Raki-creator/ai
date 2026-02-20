from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from rest_framework import status, generics, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout, get_user_model
from django.views.decorators.csrf import csrf_exempt
from .models import Chat, ChatMessage, Memory, Reminder
from .serializers import (
    UserSerializer, RegisterSerializer, LoginSerializer,
    ChatSerializer, ChatMessageSerializer,
    MemorySerializer, ReminderSerializer,
)

User = get_user_model()


# ─── Template Views ───────────────────────────────────────────────────────────

@login_required(login_url='/login/')
def dashboard_view(request):
    return render(request, 'dashboard.html', {
        'reminder_count': Reminder.objects.filter(user=request.user, completed=False).count(),
        'memory_count': Memory.objects.filter(user=request.user).count(),
    })


def login_page(request):
    if request.user.is_authenticated:
        return redirect('/')
    return render(request, 'login.html')


@login_required(login_url='/login/')
def profile_page(request):
    return render(request, 'profile.html')


@login_required(login_url='/login/')
def settings_page(request):
    return render(request, 'settings.html')


@login_required(login_url='/login/')
def memory_page(request):
    return render(request, 'memory.html')


@login_required(login_url='/login/')
def reminders_page(request):
    return render(request, 'reminders.html')

@csrf_exempt
@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def register_view(request):
    serializer = RegisterSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    user = serializer.save()
    token, _ = Token.objects.get_or_create(user=user)
    # Also log in for session authentication (templates)
    auth_login(request, user)
    return Response({
        'token': token.key,
        'user': UserSerializer(user).data,
    }, status=status.HTTP_201_CREATED)


@csrf_exempt
@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def login_view(request):
    serializer = LoginSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    user = authenticate(
        username=serializer.validated_data['email'],
        password=serializer.validated_data['password'],
    )
    if not user:
        return Response({'error': 'Invalid email or password.'}, status=status.HTTP_401_UNAUTHORIZED)

    token, _ = Token.objects.get_or_create(user=user)
    # Also log in for session authentication (templates)
    auth_login(request, user)
    return Response({
        'token': token.key,
        'user': UserSerializer(user).data,
    })


def logout_view(request):
    auth_logout(request)
    return redirect('/login/')


@api_view(['GET', 'PUT'])
def me_view(request):
    if request.method == 'GET':
        return Response(UserSerializer(request.user).data)

    serializer = UserSerializer(request.user, data=request.data, partial=True)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def password_reset_view(request):
    # Stub — in a real app, send an email
    return Response({'detail': 'Password reset is not available in local mode.'}, status=status.HTTP_200_OK)


# ─── Settings Views ──────────────────────────────────────────────────────────

@api_view(['GET', 'PUT'])
def settings_view(request):
    if request.method == 'GET':
        return Response(request.user.settings or {})

    request.user.settings = request.data
    request.user.save(update_fields=['settings'])
    return Response(request.user.settings)


# ─── Chat Views ──────────────────────────────────────────────────────────────

@api_view(['GET', 'POST'])
def chat_list(request):
    if request.method == 'GET':
        chats = Chat.objects.filter(user=request.user)
        return Response(ChatSerializer(chats, many=True).data)

    serializer = ChatSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    chat = serializer.save(user=request.user)
    return Response(ChatSerializer(chat).data, status=status.HTTP_201_CREATED)


@api_view(['GET'])
def chat_detail(request, chat_id):
    try:
        chat = Chat.objects.get(id=chat_id, user=request.user)
    except Chat.DoesNotExist:
        return Response({'error': 'Chat not found.'}, status=status.HTTP_404_NOT_FOUND)
    return Response(ChatSerializer(chat).data)


@api_view(['GET', 'POST'])
def chat_messages(request, chat_id):
    try:
        chat = Chat.objects.get(id=chat_id, user=request.user)
    except Chat.DoesNotExist:
        return Response({'error': 'Chat not found.'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        messages = chat.messages.all()
        return Response(ChatMessageSerializer(messages, many=True).data)

    serializer = ChatMessageSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    msg = serializer.save(chat=chat)

    # Update chat metadata
    chat.last_message = msg.content
    chat.save(update_fields=['last_message', 'updated_at'])

    return Response(ChatMessageSerializer(msg).data, status=status.HTTP_201_CREATED)


# ─── Memory Views ────────────────────────────────────────────────────────────

@api_view(['GET', 'POST'])
def memory_list(request):
    if request.method == 'GET':
        memories = Memory.objects.filter(user=request.user)
        return Response(MemorySerializer(memories, many=True).data)

    serializer = MemorySerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    serializer.save(user=request.user)
    return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(['DELETE'])
def memory_detail(request, memory_id):
    try:
        memory = Memory.objects.get(id=memory_id, user=request.user)
    except Memory.DoesNotExist:
        return Response({'error': 'Memory not found.'}, status=status.HTTP_404_NOT_FOUND)

    memory.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)


# ─── Reminder Views ─────────────────────────────────────────────────────────

@api_view(['GET', 'POST'])
def reminder_list(request):
    if request.method == 'GET':
        reminders = Reminder.objects.filter(user=request.user)
        return Response(ReminderSerializer(reminders, many=True).data)

    serializer = ReminderSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    serializer.save(user=request.user)
    return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(['PUT', 'DELETE'])
def reminder_detail(request, reminder_id):
    try:
        reminder = Reminder.objects.get(id=reminder_id, user=request.user)
    except Reminder.DoesNotExist:
        return Response({'error': 'Reminder not found.'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'DELETE':
        reminder.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    serializer = ReminderSerializer(reminder, data=request.data, partial=True)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(serializer.data)
