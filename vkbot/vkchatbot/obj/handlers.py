from vk_api.bot_longpoll import VkBotEventType
from vkchatbot.update import Update


def error_pacifier(bot, exc):
    pass


def pacifier(update: Update):
    pass


handlers = {VkBotEventType.MESSAGE_NEW:            pacifier,
            VkBotEventType.MESSAGE_REPLY:          pacifier,
            VkBotEventType.MESSAGE_EDIT:           pacifier,
            VkBotEventType.MESSAGE_TYPING_STATE:   pacifier,
            VkBotEventType.MESSAGE_ALLOW:          pacifier,
            VkBotEventType.MESSAGE_DENY:           pacifier,
            VkBotEventType.PHOTO_NEW:              pacifier,
            VkBotEventType.PHOTO_COMMENT_NEW:      pacifier,
            VkBotEventType.PHOTO_COMMENT_EDIT:     pacifier,
            VkBotEventType.PHOTO_COMMENT_RESTORE:  pacifier,
            VkBotEventType.PHOTO_COMMENT_DELETE:   pacifier,
            VkBotEventType.AUDIO_NEW:              pacifier,
            VkBotEventType.VIDEO_NEW:              pacifier,
            VkBotEventType.VIDEO_COMMENT_NEW:      pacifier,
            VkBotEventType.VIDEO_COMMENT_EDIT:     pacifier,
            VkBotEventType.VIDEO_COMMENT_RESTORE:  pacifier,
            VkBotEventType.VIDEO_COMMENT_DELETE:   pacifier,
            VkBotEventType.WALL_POST_NEW:          pacifier,
            VkBotEventType.WALL_REPOST:            pacifier,
            VkBotEventType.WALL_REPLY_NEW:         pacifier,
            VkBotEventType.WALL_REPLY_EDIT:        pacifier,
            VkBotEventType.WALL_REPLY_RESTORE:     pacifier,
            VkBotEventType.WALL_REPLY_DELETE:      pacifier,
            VkBotEventType.BOARD_POST_NEW:         pacifier,
            VkBotEventType.BOARD_POST_EDIT:        pacifier,
            VkBotEventType.BOARD_POST_RESTORE:     pacifier,
            VkBotEventType.BOARD_POST_DELETE:      pacifier,
            VkBotEventType.MARKET_COMMENT_NEW:     pacifier,
            VkBotEventType.MARKET_COMMENT_EDIT:    pacifier,
            VkBotEventType.MARKET_COMMENT_RESTORE: pacifier,
            VkBotEventType.MARKET_COMMENT_DELETE:  pacifier,
            VkBotEventType.GROUP_LEAVE:            pacifier,
            VkBotEventType.GROUP_JOIN:             pacifier,
            VkBotEventType.USER_BLOCK:             pacifier,
            VkBotEventType.USER_UNBLOCK:           pacifier,
            VkBotEventType.POLL_VOTE_NEW:          pacifier,
            VkBotEventType.GROUP_OFFICERS_EDIT:    pacifier,
            VkBotEventType.GROUP_CHANGE_SETTINGS:  pacifier,
            VkBotEventType.GROUP_CHANGE_PHOTO:     pacifier,
            VkBotEventType.VKPAY_TRANSACTION:      pacifier}
