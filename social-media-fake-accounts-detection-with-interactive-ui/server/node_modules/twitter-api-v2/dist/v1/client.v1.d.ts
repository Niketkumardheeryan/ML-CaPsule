/// <reference types="node" />
import { DmEventsV1Paginator, WelcomeDmV1Paginator } from '../paginators/dm.paginator.v1';
import { SendDMV1Params, DirectMessageCreateV1Result, ReceivedDMEventV1, GetDmListV1Args, MessageCreateDataV1, WelcomeDirectMessageCreateV1Result, WelcomeDmRuleV1Result, WelcomeDmRuleListV1Result, DirectMessageCreateV1 } from '../types';
import TwitterApiv1ReadWrite from './client.v1.write';
/**
 * Twitter v1.1 API client with read/write/DMs rights.
 */
export declare class TwitterApiv1 extends TwitterApiv1ReadWrite {
    protected _prefix: string;
    /**
     * Get a client with read/write rights.
     */
    get readWrite(): TwitterApiv1ReadWrite;
    /**
     * Publishes a new message_create event resulting in a Direct Message sent to a specified user from the authenticating user.
     * https://developer.twitter.com/en/docs/twitter-api/v1/direct-messages/sending-and-receiving/api-reference/new-event
     */
    sendDm({ recipient_id, custom_profile_id, ...params }: SendDMV1Params): Promise<DirectMessageCreateV1Result>;
    /**
     * Returns a single Direct Message event by the given id.
     *
     * https://developer.twitter.com/en/docs/twitter-api/v1/direct-messages/sending-and-receiving/api-reference/get-event
     */
    getDmEvent(id: string): Promise<ReceivedDMEventV1>;
    /**
     * Deletes the direct message specified in the required ID parameter.
     * The authenticating user must be the recipient of the specified direct message.
     * https://developer.twitter.com/en/docs/twitter-api/v1/direct-messages/sending-and-receiving/api-reference/delete-message-event
     */
    deleteDm(id: string): Promise<void>;
    /**
     * Returns all Direct Message events (both sent and received) within the last 30 days.
     * Sorted in reverse-chronological order.
     *
     * https://developer.twitter.com/en/docs/twitter-api/v1/direct-messages/sending-and-receiving/api-reference/list-events
     */
    listDmEvents(args?: Partial<GetDmListV1Args>): Promise<DmEventsV1Paginator>;
    /**
     * Creates a new Welcome Message that will be stored and sent in the future from the authenticating user in defined circumstances.
     * https://developer.twitter.com/en/docs/twitter-api/v1/direct-messages/welcome-messages/api-reference/new-welcome-message
     */
    newWelcomeDm(name: string, data: MessageCreateDataV1): Promise<WelcomeDirectMessageCreateV1Result>;
    /**
     * Returns a Welcome Message by the given id.
     * https://developer.twitter.com/en/docs/twitter-api/v1/direct-messages/welcome-messages/api-reference/get-welcome-message
     */
    getWelcomeDm(id: string): Promise<WelcomeDirectMessageCreateV1Result>;
    /**
     * Deletes a Welcome Message by the given id.
     * https://developer.twitter.com/en/docs/twitter-api/v1/direct-messages/welcome-messages/api-reference/delete-welcome-message
     */
    deleteWelcomeDm(id: string): Promise<void>;
    /**
     * Updates a Welcome Message by the given ID.
     * Updates to the welcome_message object are atomic.
     * https://developer.twitter.com/en/docs/twitter-api/v1/direct-messages/welcome-messages/api-reference/update-welcome-message
     */
    updateWelcomeDm(id: string, data: MessageCreateDataV1): Promise<WelcomeDirectMessageCreateV1Result>;
    /**
     * Returns all Direct Message events (both sent and received) within the last 30 days.
     * Sorted in reverse-chronological order.
     *
     * https://developer.twitter.com/en/docs/twitter-api/v1/direct-messages/sending-and-receiving/api-reference/list-events
     */
    listWelcomeDms(args?: Partial<GetDmListV1Args>): Promise<WelcomeDmV1Paginator>;
    /**
     * Creates a new Welcome Message Rule that determines which Welcome Message will be shown in a given conversation.
     * https://developer.twitter.com/en/docs/twitter-api/v1/direct-messages/welcome-messages/api-reference/new-welcome-message-rule
     */
    newWelcomeDmRule(welcomeMessageId: string): Promise<WelcomeDmRuleV1Result>;
    /**
     * Returns a Welcome Message Rule by the given id.
     * https://developer.twitter.com/en/docs/twitter-api/v1/direct-messages/welcome-messages/api-reference/get-welcome-message-rule
     */
    getWelcomeDmRule(id: string): Promise<WelcomeDmRuleV1Result>;
    /**
     * Deletes a Welcome Message Rule by the given id.
     * https://developer.twitter.com/en/docs/twitter-api/v1/direct-messages/welcome-messages/api-reference/delete-welcome-message-rule
     */
    deleteWelcomeDmRule(id: string): Promise<void>;
    /**
     * Retrieves all welcome DM rules for this account.
     * https://developer.twitter.com/en/docs/twitter-api/v1/direct-messages/welcome-messages/api-reference/list-welcome-message-rules
     */
    listWelcomeDmRules(args?: Partial<GetDmListV1Args>): Promise<WelcomeDmRuleListV1Result>;
    /**
     * Set the current showed welcome message for logged account ; wrapper for Welcome DM rules.
     * Test if a rule already exists, delete if any, then create a rule for current message ID.
     *
     * If you don't have already a welcome message, create it with `.newWelcomeMessage`.
     */
    setWelcomeDm(welcomeMessageId: string, deleteAssociatedWelcomeDmWhenDeletingRule?: boolean): Promise<WelcomeDmRuleV1Result>;
    /**
     * Marks a message as read in the recipient’s Direct Message conversation view with the sender.
     * https://developer.twitter.com/en/docs/twitter-api/v1/direct-messages/typing-indicator-and-read-receipts/api-reference/new-read-receipt
     */
    markDmAsRead(lastEventId: string, recipientId: string): Promise<void>;
    /**
     * Displays a visual typing indicator in the recipient’s Direct Message conversation view with the sender.
     * https://developer.twitter.com/en/docs/twitter-api/v1/direct-messages/typing-indicator-and-read-receipts/api-reference/new-typing-indicator
     */
    indicateDmTyping(recipientId: string): Promise<void>;
    /**
     * Get a single image attached to a direct message. TwitterApi client must be logged with OAuth 1.0a.
     * https://developer.twitter.com/en/docs/twitter-api/v1/direct-messages/message-attachments/guides/retrieving-media
     */
    downloadDmImage(urlOrDm: string | DirectMessageCreateV1): Promise<Buffer>;
}
export default TwitterApiv1;
