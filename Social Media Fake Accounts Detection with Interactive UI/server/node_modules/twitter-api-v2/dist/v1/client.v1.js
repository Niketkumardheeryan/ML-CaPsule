"use strict";
var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
Object.defineProperty(exports, "__esModule", { value: true });
exports.TwitterApiv1 = void 0;
const globals_1 = require("../globals");
const dm_paginator_v1_1 = require("../paginators/dm.paginator.v1");
const types_1 = require("../types");
const client_v1_write_1 = __importDefault(require("./client.v1.write"));
/**
 * Twitter v1.1 API client with read/write/DMs rights.
 */
class TwitterApiv1 extends client_v1_write_1.default {
    constructor() {
        super(...arguments);
        this._prefix = globals_1.API_V1_1_PREFIX;
    }
    /**
     * Get a client with read/write rights.
     */
    get readWrite() {
        return this;
    }
    /* Direct messages */
    // Part: Sending and receiving events
    /**
     * Publishes a new message_create event resulting in a Direct Message sent to a specified user from the authenticating user.
     * https://developer.twitter.com/en/docs/twitter-api/v1/direct-messages/sending-and-receiving/api-reference/new-event
     */
    sendDm({ recipient_id, custom_profile_id, ...params }) {
        const args = {
            event: {
                type: types_1.EDirectMessageEventTypeV1.Create,
                [types_1.EDirectMessageEventTypeV1.Create]: {
                    target: { recipient_id },
                    message_data: params,
                },
            },
        };
        if (custom_profile_id) {
            args.event[types_1.EDirectMessageEventTypeV1.Create].custom_profile_id = custom_profile_id;
        }
        return this.post('direct_messages/events/new.json', args, {
            forceBodyMode: 'json',
        });
    }
    /**
     * Returns a single Direct Message event by the given id.
     *
     * https://developer.twitter.com/en/docs/twitter-api/v1/direct-messages/sending-and-receiving/api-reference/get-event
     */
    getDmEvent(id) {
        return this.get('direct_messages/events/show.json', { id });
    }
    /**
     * Deletes the direct message specified in the required ID parameter.
     * The authenticating user must be the recipient of the specified direct message.
     * https://developer.twitter.com/en/docs/twitter-api/v1/direct-messages/sending-and-receiving/api-reference/delete-message-event
     */
    deleteDm(id) {
        return this.delete('direct_messages/events/destroy.json', { id });
    }
    /**
     * Returns all Direct Message events (both sent and received) within the last 30 days.
     * Sorted in reverse-chronological order.
     *
     * https://developer.twitter.com/en/docs/twitter-api/v1/direct-messages/sending-and-receiving/api-reference/list-events
     */
    async listDmEvents(args = {}) {
        const queryParams = { ...args };
        const initialRq = await this.get('direct_messages/events/list.json', queryParams, { fullResponse: true });
        return new dm_paginator_v1_1.DmEventsV1Paginator({
            realData: initialRq.data,
            rateLimit: initialRq.rateLimit,
            instance: this,
            queryParams,
        });
    }
    // Part: Welcome messages (events)
    /**
     * Creates a new Welcome Message that will be stored and sent in the future from the authenticating user in defined circumstances.
     * https://developer.twitter.com/en/docs/twitter-api/v1/direct-messages/welcome-messages/api-reference/new-welcome-message
     */
    newWelcomeDm(name, data) {
        const args = {
            [types_1.EDirectMessageEventTypeV1.WelcomeCreate]: {
                name,
                message_data: data,
            },
        };
        return this.post('direct_messages/welcome_messages/new.json', args, {
            forceBodyMode: 'json',
        });
    }
    /**
     * Returns a Welcome Message by the given id.
     * https://developer.twitter.com/en/docs/twitter-api/v1/direct-messages/welcome-messages/api-reference/get-welcome-message
     */
    getWelcomeDm(id) {
        return this.get('direct_messages/welcome_messages/show.json', { id });
    }
    /**
     * Deletes a Welcome Message by the given id.
     * https://developer.twitter.com/en/docs/twitter-api/v1/direct-messages/welcome-messages/api-reference/delete-welcome-message
     */
    deleteWelcomeDm(id) {
        return this.delete('direct_messages/welcome_messages/destroy.json', { id });
    }
    /**
     * Updates a Welcome Message by the given ID.
     * Updates to the welcome_message object are atomic.
     * https://developer.twitter.com/en/docs/twitter-api/v1/direct-messages/welcome-messages/api-reference/update-welcome-message
     */
    updateWelcomeDm(id, data) {
        const args = { message_data: data };
        return this.put('direct_messages/welcome_messages/update.json', args, {
            forceBodyMode: 'json',
            query: { id },
        });
    }
    /**
     * Returns all Direct Message events (both sent and received) within the last 30 days.
     * Sorted in reverse-chronological order.
     *
     * https://developer.twitter.com/en/docs/twitter-api/v1/direct-messages/sending-and-receiving/api-reference/list-events
     */
    async listWelcomeDms(args = {}) {
        const queryParams = { ...args };
        const initialRq = await this.get('direct_messages/welcome_messages/list.json', queryParams, { fullResponse: true });
        return new dm_paginator_v1_1.WelcomeDmV1Paginator({
            realData: initialRq.data,
            rateLimit: initialRq.rateLimit,
            instance: this,
            queryParams,
        });
    }
    // Part: Welcome message (rules)
    /**
     * Creates a new Welcome Message Rule that determines which Welcome Message will be shown in a given conversation.
     * https://developer.twitter.com/en/docs/twitter-api/v1/direct-messages/welcome-messages/api-reference/new-welcome-message-rule
     */
    newWelcomeDmRule(welcomeMessageId) {
        return this.post('direct_messages/welcome_messages/rules/new.json', {
            welcome_message_rule: { welcome_message_id: welcomeMessageId },
        }, {
            forceBodyMode: 'json',
        });
    }
    /**
     * Returns a Welcome Message Rule by the given id.
     * https://developer.twitter.com/en/docs/twitter-api/v1/direct-messages/welcome-messages/api-reference/get-welcome-message-rule
     */
    getWelcomeDmRule(id) {
        return this.get('direct_messages/welcome_messages/rules/show.json', { id });
    }
    /**
     * Deletes a Welcome Message Rule by the given id.
     * https://developer.twitter.com/en/docs/twitter-api/v1/direct-messages/welcome-messages/api-reference/delete-welcome-message-rule
     */
    deleteWelcomeDmRule(id) {
        return this.delete('direct_messages/welcome_messages/rules/destroy.json', { id });
    }
    /**
     * Retrieves all welcome DM rules for this account.
     * https://developer.twitter.com/en/docs/twitter-api/v1/direct-messages/welcome-messages/api-reference/list-welcome-message-rules
     */
    async listWelcomeDmRules(args = {}) {
        const queryParams = { ...args };
        return this.get('direct_messages/welcome_messages/rules/list.json', queryParams);
    }
    /**
     * Set the current showed welcome message for logged account ; wrapper for Welcome DM rules.
     * Test if a rule already exists, delete if any, then create a rule for current message ID.
     *
     * If you don't have already a welcome message, create it with `.newWelcomeMessage`.
     */
    async setWelcomeDm(welcomeMessageId, deleteAssociatedWelcomeDmWhenDeletingRule = true) {
        var _a;
        const existingRules = await this.listWelcomeDmRules();
        if ((_a = existingRules.welcome_message_rules) === null || _a === void 0 ? void 0 : _a.length) {
            for (const rule of existingRules.welcome_message_rules) {
                await this.deleteWelcomeDmRule(rule.id);
                if (deleteAssociatedWelcomeDmWhenDeletingRule) {
                    await this.deleteWelcomeDm(rule.welcome_message_id);
                }
            }
        }
        return this.newWelcomeDmRule(welcomeMessageId);
    }
    // Part: Read indicator
    /**
     * Marks a message as read in the recipient’s Direct Message conversation view with the sender.
     * https://developer.twitter.com/en/docs/twitter-api/v1/direct-messages/typing-indicator-and-read-receipts/api-reference/new-read-receipt
     */
    markDmAsRead(lastEventId, recipientId) {
        return this.post('direct_messages/mark_read.json', {
            last_read_event_id: lastEventId,
            recipient_id: recipientId,
        }, { forceBodyMode: 'url' });
    }
    /**
     * Displays a visual typing indicator in the recipient’s Direct Message conversation view with the sender.
     * https://developer.twitter.com/en/docs/twitter-api/v1/direct-messages/typing-indicator-and-read-receipts/api-reference/new-typing-indicator
     */
    indicateDmTyping(recipientId) {
        return this.post('direct_messages/indicate_typing.json', {
            recipient_id: recipientId,
        }, { forceBodyMode: 'url' });
    }
    // Part: Images
    /**
     * Get a single image attached to a direct message. TwitterApi client must be logged with OAuth 1.0a.
     * https://developer.twitter.com/en/docs/twitter-api/v1/direct-messages/message-attachments/guides/retrieving-media
     */
    async downloadDmImage(urlOrDm) {
        if (typeof urlOrDm !== 'string') {
            const attachment = urlOrDm[types_1.EDirectMessageEventTypeV1.Create].message_data.attachment;
            if (!attachment) {
                throw new Error('The given direct message doesn\'t contain any attachment');
            }
            urlOrDm = attachment.media_url_https;
        }
        const data = await this.get(urlOrDm, undefined, { forceParseMode: 'buffer', prefix: '' });
        if (!data.length) {
            throw new Error('Image not found. Make sure you are logged with credentials able to access direct messages, and check the URL.');
        }
        return data;
    }
}
exports.TwitterApiv1 = TwitterApiv1;
exports.default = TwitterApiv1;
