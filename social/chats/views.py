from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from chats.models import Chat
from django.http import JsonResponse
from chats.forms import MesasageForm
from django.contrib.auth import get_user_model

User = get_user_model()

@login_required
def chat_list(request):
    chats = request.user.chats.all()
    return render(request, 'chats/chat_list.html', {'chats':chats})

@login_required
def chat_detail(request, chat_id):
    chat = get_object_or_404(Chat, id=chat_id)
    if request.user not in chat.participants.all():
        return redirect('chat_detail', chat_id=chat.id)
    messages = chat.messages.all()
    form = MesasageForm()  # Добавляем форму
    return render(request, 'chats/chat_detail.html', {'chat': chat, 'messages': messages, 'form': form})

@login_required
def send_message(request, chat_id):
    chat = get_object_or_404(Chat, id=chat_id)
    if request.user not in chat.participants.all():
        return JsonResponse({'error':'You are not a participant of this chat.'}, status=403)
    if request.method == 'POST':
        form = MesasageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.chat = chat
            message.sender = request.user
            message.save()
            return JsonResponse({'message': 'Message sent successfully!'})
    return JsonResponse({'error': 'Invalid request.'}, status=400)


@login_required
def start_chat(request, user_id):
    other_user = get_object_or_404(User, id=user_id)
    chat = Chat.objects.filter(participants=request.user).filter(participants=other_user).first()
    if not chat:
        chat = Chat.objects.create()
        chat.participants.add(request.user, other_user)
    return redirect('chat_detail', chat_id=chat.id)