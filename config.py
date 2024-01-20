# BOT INFOS
token = '6832362422:AAHD5XHEqutLZkxnI41--SXYbQQ36PidUdo'
channel_username = "@spliptv"

# MySQL Database
mysql_host = 'localhost'
mysql_db   = 'TelegramSupportBot'
mysql_user = 'SupportBotUser'
mysql_pw   = 'jlargueze'

# Support Chat (Chat ID)/ Owner (Jordy ID)
support_chat = -1002130364079
owner = 703053891 
user_sessions = {}

# Divers
time_zone           = 'GMT+1'   
bad_words_toggle    = True      
spam_toggle         = True 
spam_protection     = 5
open_ticket_emoji   = 24

# Messages Dict
text_messages = {
    'start': {
        'en': '🌟 Welcome to SPL IPTV! 🌟\n\n🔒 Why Subscribe?\nExclusive Content: Access unique content, in-depth analyses, and firsthand information that you won\'t find anywhere else.\n\nReal-Time Updates: Always stay updated with the latest news, trends, and most recent analyses in the field you appreciate.\n\nMulti-Screen Experience: Depending on your package, you can access our content on 1, 2, or even 3 screens simultaneously, perfect for families or groups.\n\n💰 Prices and Subscriptions 💰\n\n📅 1-Year Subscription:\n1 screen: 60 euros\n2 screens: 95 euros\n3 screens: 125 euros\n\n📆 6-Month Subscription:\n1 screen: 35 euros\n\n⏳ 3-Month Subscription:1 screen: 25 euros\n\n🛡️ How to Subscribe?\n\nSelect Your Package: Choose an option that best suits your needs and budget.\n\nProceed with Payment: Follow the instructions to make your payment securely.\n\nJoin the Community: Once your subscription is confirmed, you\'ll have access to all the exclusive benefits reserved for members.\n\n📧 Customer Support:\n\nFor any questions or concerns, don\'t hesitate to contact us at [email address or other contact method].\n\n🔗 Join us today and never miss an update!',
        'fr': '🌟 Bienvenue sur SPL IPTV ! 🌟\n\n🔒 Pourquoi vous abonner ?\nContenu Exclusif : Accédez à des contenus uniques, des analyses approfondies et des informations de première main que vous ne trouverez nulle part ailleurs.\n\nMise à jour en Temps Réel : Soyez toujours au courant des dernières actualités, des tendances et des analyses les plus récentes dans le domaine que vous appréciez.\n\nExpérience Multi-Écran : Selon votre forfait, vous pouvez accéder à notre contenu sur 1, 2 ou même 3 écrans simultanément, idéal pour les familles ou les groupes.\n\n💰 Prix et Abonnements 💰\n\n📅 Abonnement 1 an :\n1 écran : 60 euros\n2 écrans : 95 euros\n3 écrans : 125 euros\n\n📆 Abonnement de 6 mois :\n1 écran : 35 euros\n\n⏳ Abonnement de 3 mois :\n1 écran : 25 euros\n\n🛡️ Comment être abonner ?\n\nSélectionnez votre forfait : Choisissez une option qui vous convient le mieux en fonction de vos besoins et de votre budget.\n\nProcédez au paiement : Suivez les instructions pour effectuer votre paiement de manière sécurisée.\n\nRejoignez la communauté : Une fois votre abonnement confirmé, vous aurez accès à tous les avantages exclusifs réservés aux membres.\n\n📧 Support Client :\n\nPour toute question ou préoccupation, hésitez pas à nous contacter à [adresse e-mail ou autre moyen de contact].\n\n🔗 Rejoignez-nous dès aujourd''hui et ne manquez jamais une mise à jour !',
    },
   'help': {
        'en': '👋 Hello! Please explain clearly what is happening to you. Our support team is here to help! 🆘',
        'fr': '👋 Bonjour ! Merci d\'expliquer explicitement ce qu\'il vous arrive. Notre équipe de support est là pour vous aider ! 🆘',
    },
    'year': {
        'en': '🎉 Congratulations on choosing our premium 1-year package at 60 euros! This incredible offer translates to just 5 euros per month.\nUnlock even more value with our additional screen options:\n\n1 screen - Basic package at 60 euros\n2 screens - Enhanced package at 95 euros\n3 screens - Premium package at 125 euros.\n\nSelect the option that best suits your needs and enjoy the exclusive content we have in store for you! 🌟',
        'fr': '🎉 Félicitations d\'avoir choisi notre forfait premium d\'1 an à 60 euros ! Cette offre exceptionnelle revient à seulement 5 euros par mois.\nDébloquez encore plus de valeur avec nos options d\'écrans supplémentaires :\n\n1 écran - Forfait de base à 60 euros\n2 écrans - Forfait amélioré à 95 euros\n3 écrans - Forfait premium à 125 euros.\n\nChoisissez l\'option qui correspond le mieux à vos besoins et profitez du contenu exclusif que nous avons préparé pour vous ! 🌟',
    },
    'semester': {
        'en': '🎉 Congratulations on choosing our flexible 6-month package at 35 euros! This amazing offer breaks down to approximately 5.83 euros per month.\nThank you for choosing our service! Please proceed with the payment using your preferred method. 💳',
        'fr': '🎉 Félicitations d\'avoir choisi notre forfait souple de 6 mois à 35 euros ! Cette offre exceptionnelle revient à environ 5,83 euros par mois.\nMerci d\'avoir choisi notre service ! Veuillez procéder au paiement en utilisant votre méthode préférée. 💳',
    },
    'quarter': {
        'en': '🎉 Congratulations on choosing our convenient 3-month package at 25 euros! This fantastic offer translates to approximately 8.33 euros per month.\nThank you for choosing our service! Please proceed with the payment using your preferred method. 💳',
        'fr': '🎉 Félicitations d\'avoir choisi notre forfait pratique de 3 mois à 25 euros ! Cette offre exceptionnelle revient à environ 8,33 euros par mois.\nMerci d\'avoir choisi notre service ! Veuillez procéder au paiement en utilisant votre méthode préférée. 💳',
    },
    'screen_choice': {
        'en': 'You have chosen the one-year subscription with {}.\nThank you for choosing our service! Please proceed with the payment using your preferred method. 💳',
        'fr': 'Vous avez choisi l\'abonnement d\'un an avec {}.\nMerci d\'avoir choisi notre service ! Veuillez procéder au paiement en utilisant votre méthode préférée. 💳',
    },
    'payment': {
        'en': 'Choose your payment method:',
        'fr': 'Choisissez votre mode de paiement :',
    },
    'bitcoin_payment': {
        'en': '💰 BitCoin Payment: 3NBNX8YrW3HRhfGhFNpwC8Vvq5SMpxwRVt\nThank you for choosing the secure and decentralized payment option! 🌐',
        'fr': '💰 Paiement BitCoin : 3NBNX8YrW3HRhfGhFNpwC8Vvq5SMpxwRVt\nMerci d\'avoir choisi l\'option de paiement sécurisée et décentralisée ! 🌐',
    },
    'paypal_payment': {
        'en': '💰 PayPal Payment: spliptvontelegram@gmail.com\nThank you for choosing the convenient and widely accepted PayPal payment option! 💳',
        'fr': '💰 Paiement PayPal : spliptvontelegram@gmail.com\nMerci d\'avoir choisi l\'option de paiement PayPal, pratique et largement acceptée ! 💳',
    },
    'payment_confirmation': {
        'en': 'Payment completed! A support agent will assist you shortly.',
        'fr': 'Paiement effectué ! Un agent du support vous assistera sous peu.',
    },
    'support_response': '🚨 Support : '
}

regex_filter = {
    'bad_words': r'(?i)^(.*?(\b\w*fuck|shut up|dick|bitch|bastart|cunt|bollocks|bugger|rubbish|wanker|twat|suck|ass|pussy|arsch\w*\b)[^$]*)$'
}
