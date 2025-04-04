css = '''
<style>
.chat-message {
    padding: 1.5rem; border-radius: 0.5rem; margin-bottom: 1rem; display: flex
}
.chat-message.user {
    background-color: #2b313e
}
.chat-message.bot {
    background-color: #475063
}
.chat-message .avatar {
  width: 20%;
}
.chat-message .avatar img {
  max-width: 60px;
  max-height: 60px;
  border-radius: 50%;
  object-fit: cover;
}
.chat-message .message {
  width: 80%;
  padding: 0 1.5rem;
  color: #fff;
}
'''

bot_template = '''
<div class="chat-message bot">
    <div class="avatar">
        <img src="https://img.freepik.com/free-vector/cartoon-style-robot-vectorart_78370-4103.jpg?t=st=1743752887~exp=1743756487~hmac=33cf022934f6de384b0985618447f15cfb9e7b3ee7d212cde1d5ac47dc87ae79&w=740">
    </div>
    <div class="message">{{MSG}}</div>
</div>
'''

user_template = '''
<div class="chat-message user">
    <div class="avatar">
        <img src="https://img.freepik.com/free-vector/user-blue-gradient_78370-4692.jpg?t=st=1743753092~exp=1743756692~hmac=88753735bb61d71e7221ae17cbe1b72313b127a4ad836437e8e8162ec9f32806&w=740">
    </div>    
    <div class="message">{{MSG}}</div>
</div>
'''