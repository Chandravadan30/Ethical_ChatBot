import os
import random
from dotenv import load_dotenv
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, CallbackQueryHandler, filters, ContextTypes
import openai

# Load environment variables
load_dotenv()
TELEGRAM_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
OPENAI_KEY = os.getenv("OPENAI_API_KEY")

# OpenAI client
client = openai.OpenAI(api_key=OPENAI_KEY)

# Ethical dilemmas (25 items)
dilemmas = [
    "A school uses AI to predict student performance and decides who gets extra help. Is this ethical?",
    "A smart fridge tracks what you eat and sells that data to insurance companies. Is this fair?",
    "An app collects location data even when it's not open. Should it be allowed?",
    "A company uses voice assistants to monitor employee productivity. Should this be allowed?",
    "A developer refuses to build surveillance software for moral reasons. Is that professional?",
    "A fitness app shares user health data with advertisers without consent. Is that acceptable?",
    "An algorithm denies loan applications based on zip codes. Is this discriminatory?",
    "A university uses proctoring software that accesses webcams and microphones. Is it invasive?",
    "A hiring algorithm favors male candidates over female ones. Should it be used?",
    "A smart speaker records background conversations and stores them indefinitely. Is this ethical?",
    "A hospital uses AI to triage patients, prioritizing cost-saving outcomes. Is that justifiable?",
    "An AI chatbot gives mental health advice without disclaimers. Is that safe?",
    "A social media platform collects facial data from all uploaded photos. Should it disclose this?",
    "A school uses AI to monitor student screens during exams. Is this a privacy violation?",
    "A shopping website tracks mouse movements to predict purchase behavior. Is this transparent?",
    "An AI judges art contest submissions. Is artistic judgment something AI should perform?",
    "A company reuses customer emails to train an AI model without notification. Is this fair use?",
    "A city uses facial recognition on public transit to reduce fare evasion. Is this overreach?",
    "A dating app matches users based on personality and private message analysis. Is that okay?",
    "An online course provider ranks students by engagement time and sells this to employers. Ethical?",
    "A museum replaces human guides with AI avatars that record visitor reactions. Is this right?",
    "A government agency uses predictive models to flag citizens as 'risky' for investigation. Is this ethical?",
    "An AI music composer generates songs based on patterns from copyrighted music. Is this fair?",
    "A teacher uses ChatGPT to grade essays quickly. Are students being fairly assessed?",
    "A workplace uses AI mood detection cameras. Can this affect employee trust?"
]

# Multiple choice quiz questions (25 items)
quiz_questions = [
    {
        "question": "Which of the following is NOT a principle of data ethics?",
        "options": ["Transparency", "Consent", "Profit Maximization", "Accountability"],
        "answer": "Profit Maximization",
        "explanation": "Profit Maximization is a business objective, not a core value of ethical data use like transparency or accountability."
    },
    {
        "question": "What is the main concern with facial recognition in public spaces?",
        "options": ["It looks cool", "It’s fast", "Privacy invasion", "It helps marketing"],
        "answer": "Privacy invasion",
        "explanation": "Facial recognition can be used to track people without their consent, raising serious privacy concerns."
    },
    {
        "question": "What does the principle of 'data minimization' mean?",
        "options": ["Collect as much data as possible", "Only collect data you really need", "Share all data", "Encrypt everything"],
        "answer": "Only collect data you really need",
        "explanation": "Data minimization encourages limiting data collection to only what’s necessary for a specific purpose."
    },
    {
        "question": "What is 'algorithmic bias'?",
        "options": ["When AI makes fair choices", "When data is stored incorrectly", "When AI discriminates unfairly", "A type of computer memory"],
        "answer": "When AI discriminates unfairly",
        "explanation": "Algorithmic bias happens when a system shows unfair favoritism or discrimination due to biased data or design."
    },
    {
        "question": "Why is user consent important in data collection?",
        "options": ["It’s legally required", "It builds trust", "It respects autonomy", "All of the above"],
        "answer": "All of the above",
        "explanation": "Consent protects rights, builds trust, and ensures legal and ethical data use."
    },
    {
        "question": "What is the risk of using only historical data in AI systems?",
        "options": ["Improved accuracy", "Bias reinforcement", "Better speed", "Data loss"],
        "answer": "Bias reinforcement",
        "explanation": "Historical data can contain biases, which AI might repeat and reinforce."
    },
    {
        "question": "Which of these is an example of ethical data use?",
        "options": ["Selling emails without consent", "Analyzing anonymous feedback", "Sharing phone numbers", "Monitoring webcams secretly"],
        "answer": "Analyzing anonymous feedback",
        "explanation": "Anonymous feedback respects privacy while still providing useful insights."
    },
    {
        "question": "What does 'data transparency' mean?",
        "options": ["Hiding sensitive data", "Letting users know how data is used", "Encrypting all data", "Tracking browsing history"],
        "answer": "Letting users know how data is used",
        "explanation": "Transparency involves being open about data collection and use."
    },
    {
        "question": "What is 'informed consent'?",
        "options": ["Forcing users to agree", "Notifying users after data is taken", "Giving users a clear choice before collecting data", "Hidden privacy policies"],
        "answer": "Giving users a clear choice before collecting data",
        "explanation": "Informed consent requires users to clearly understand and agree to data practices before collection."
    },
    {
        "question": "Why is explainability important in AI?",
        "options": ["To make the model faster", "So users understand decisions", "To reduce code", "To increase profit"],
        "answer": "So users understand decisions",
        "explanation": "Explainable AI builds trust and allows users to understand how decisions are made."
    },
    {
        "question": "What is the ethical issue with predictive policing?",
        "options": ["It’s too slow", "It leads to bias and discrimination", "It reduces crime", "It’s only used in big cities"],
        "answer": "It leads to bias and discrimination",
        "explanation": "Predictive policing can reinforce existing racial or geographic biases in law enforcement."
    },
    {
        "question": "Which one is NOT an ethical concern in data science?",
        "options": ["Bias", "Privacy", "Transparency", "Revenue growth"],
        "answer": "Revenue growth",
        "explanation": "Revenue growth is a business goal, not an ethical value in data science."
    },
    {
        "question": "What makes an AI model 'fair'?",
        "options": ["It favors high-income groups", "It gives different results to different people", "It treats all users equitably", "It’s faster than others"],
        "answer": "It treats all users equitably",
        "explanation": "Fair models make decisions that do not favor or harm specific groups unfairly."
    },
    {
        "question": "What should a company do before collecting user data?",
        "options": ["Get informed consent", "Use hidden trackers", "Export it abroad", "Encrypt later"],
        "answer": "Get informed consent",
        "explanation": "Ethical data collection starts with getting clear, informed permission from users."
    },
    {
        "question": "What is the danger of black-box models?",
        "options": ["They’re open source", "Nobody can understand their decisions", "They use small data", "They take longer to train"],
        "answer": "Nobody can understand their decisions",
        "explanation": "Black-box models lack transparency, making their decisions hard to audit or explain."
    },
    {
        "question": "What is data anonymization?",
        "options": ["Deleting data", "Replacing identities with fake ones", "Storing data in Excel", "Sending to cloud"],
        "answer": "Replacing identities with fake ones",
        "explanation": "Anonymization removes or alters identifying details so individuals cannot be traced."
    },
    {
        "question": "Who is responsible for AI decisions?",
        "options": ["The programmer", "The user", "The company or organization", "Nobody"],
        "answer": "The company or organization",
        "explanation": "Organizations are accountable for deploying and overseeing responsible use of AI."
    },
    {
        "question": "Which value is MOST important when using data to make hiring decisions?",
        "options": ["Accuracy", "Speed", "Fairness", "Profit"],
        "answer": "Fairness",
        "explanation": "Fairness ensures hiring practices do not disadvantage protected or minority groups."
    },
    {
        "question": "Which of the following helps prevent bias in datasets?",
        "options": ["Collecting diverse data", "Ignoring race/gender", "Using older datasets", "Choosing only positive cases"],
        "answer": "Collecting diverse data",
        "explanation": "Diverse datasets reduce the risk of reinforcing one-sided or discriminatory outcomes."
    },
    {
        "question": "What should AI systems avoid in ethical design?",
        "options": ["Bias", "Transparency", "Consent", "Security"],
        "answer": "Bias",
        "explanation": "Bias leads to unfair outcomes and is the opposite of ethical AI behavior."
    },
    {
        "question": "Which of these is a GDPR principle?",
        "options": ["Minimal processing", "Maximized profiling", "Mandatory tracking", "Random consent"],
        "answer": "Minimal processing",
        "explanation": "GDPR promotes collecting only the minimal data necessary for the intended purpose."
    },
    {
        "question": "If a model uses personal health data, it must...",
        "options": ["Use open source", "Be HIPAA compliant", "Be fast", "Encrypt output only"],
        "answer": "Be HIPAA compliant",
        "explanation": "HIPAA ensures that health data is handled according to strict privacy standards."
    },
    {
        "question": "Which of the following is a 'soft' ethical principle?",
        "options": ["Empathy", "Privacy", "Compliance", "Encryption"],
        "answer": "Empathy",
        "explanation": "Empathy reflects compassion and understanding — it guides ethical decision-making beyond rules."
    },
    {
        "question": "An AI model selects scholarship recipients based on social media activity. This is a...",
        "options": ["Fair algorithm", "Violation of autonomy", "Good use of big data", "GDPR compliance"],
        "answer": "Violation of autonomy",
        "explanation": "Making decisions based on private behavior violates the user’s freedom and consent."
    },
    {
        "question": "Which group is most at risk from algorithmic bias?",
        "options": ["Privileged users", "Historically marginalized communities", "Robots", "IT professionals"],
        "answer": "Historically marginalized communities",
        "explanation": "Bias often reinforces historical inequalities and disproportionately impacts disadvantaged groups."
    }
]
# Start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 I’m Ethical Chatbot Bot.\nType:\n'Scenario' for Ethical Dilemmas\n'Quiz', 'Another question', or 'Test me' for a quiz\nor Ask any question about Data ethics!"
    )

# Handle user messages
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.lower().strip()

    # Prevent users from typing Yes/No/Unsure manually
    if text in ["yes", "no", "unsure"]:
        await update.message.reply_text("Please use the buttons below to respond to the dilemma.")
        return

    if "scenario" in text:
        dilemma = random.choice(dilemmas)
        keyboard = [
            [InlineKeyboardButton("Yes", callback_data="Yes"),
             InlineKeyboardButton("No", callback_data="No"),
             InlineKeyboardButton("Unsure", callback_data="Unsure")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await update.message.reply_text(f"🧐 Ethical Dilemma:\n{dilemma}", reply_markup=reply_markup)

    elif any(word in text for word in ["quiz", "another question", "next question", "give me one", "one more", "test me"]):
        q = random.choice(quiz_questions)
        options = [[InlineKeyboardButton(opt, callback_data=f"quiz_{opt}")] for opt in q["options"]]
        context.user_data["quiz_answer"] = q["answer"]
        await update.message.reply_text(f"🧠 Quiz:\n{q['question']}", reply_markup=InlineKeyboardMarkup(options))

    elif context.user_data.get("expecting_reflection"):
        context.user_data["expecting_reflection"] = False
        prompt = f"""You are an assistant helping users reflect on ethical dilemmas.\nUser said: \"{update.message.text}\"\nReply in 1-2 short sentences, supporting their view and highlighting the value they mentioned."""

        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=200,
            temperature=0.7
        )
        await update.message.reply_text(response.choices[0].message.content.strip())

    else:
        prompt = f"""You are a helpful assistant that explains ethical issues in data.\nAnswer this clearly: {update.message.text}"""
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=200,
            temperature=0.7
        )
        await update.message.reply_text(response.choices[0].message.content.strip())

# Handle button responses
async def handle_buttons(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    response = query.data

    async def handle_buttons(update: Update, context: ContextTypes.DEFAULT_TYPE):
        query = update.callback_query
    await query.answer()

    response = query.data

    if response.startswith("quiz_"):
        selected = response.split("_", 1)[1]
        correct = context.user_data.get("quiz_answer", "")
        question_obj = next((q for q in quiz_questions if q["answer"] == correct), None)
        explanation = question_obj.get("explanation", "No explanation available.") if question_obj else ""

        if selected == correct:
            await query.edit_message_text(f"✅ Correct! The answer is: {correct}\n\n💡 Explanation: {explanation}")
        else:
            await query.edit_message_text(f"❌ Incorrect. The right answer is: {correct}\n\n💡 Explanation: {explanation}")

    else:
        # This is for scenario responses (Yes/No/Unsure)
        await query.edit_message_text(f"📌 You selected: {response}")

        reflection_prompt = f"You selected '{response}' for the ethical dilemma. What ethical concerns might support this response? Think about privacy, fairness, or transparency."

        await query.message.reply_text(f"🤔 {reflection_prompt}")
        context.user_data["expecting_reflection"] = True

# Main app runner
if __name__ == '__main__':
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.add_handler(CallbackQueryHandler(handle_buttons))

    print("✅ Ethical chatbot is running...")
    app.run_polling()

