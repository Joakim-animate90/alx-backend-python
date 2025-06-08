from chats.models import User, Conversation

# Create dummy users
user1, created1 = User.objects.get_or_create(
    username='alice',
    defaults={
        'email': 'alice@example.com',
        'first_name': 'Alice',
        'last_name': 'Smith',
        'phone_number': '+12345678901',
    }
)
user2, created2 = User.objects.get_or_create(
    username='bob',
    defaults={
        'email': 'bob@example.com',
        'first_name': 'Bob',
        'last_name': 'Jones',
        'phone_number': '+19876543210',
    }
)

# Create a conversation between them
conv, created_conv = Conversation.objects.get_or_create()
conv.participants.set([user1, user2])
conv.save()

print("Dummy users and conversation created.")
print("User 1 UUID:", user1.user_id)
print("User 2 UUID:", user2.user_id)
print("Conversation UUID:", conv.conversation_id)
