import TwitterApiSubClient from '../client.subclient';
import { FilterStreamV1Params, SampleStreamV1Params, UserV1, VerifyCredentialsV1Params, AppRateLimitV1Result, TAppRateLimitResourceV1, HelpLanguageV1Result, ReverseGeoCodeV1Params, ReverseGeoCodeV1Result, PlaceV1, SearchGeoV1Params, SearchGeoV1Result, TrendMatchV1, TrendsPlaceV1Params, TrendLocationV1, TweetV1TimelineParams, TweetV1UserTimelineParams, TweetV1, MediaStatusV1Result, OembedTweetV1Params, OembedTweetV1Result, MuteUserListV1Params, MuteUserIdsV1Params, UserSearchV1Params, AccountSettingsV1, ProfileBannerSizeV1, ProfileBannerSizeV1Params, FriendshipLookupV1Params, FriendshipLookupV1, FriendshipShowV1Params, FriendshipV1, FriendshipsIncomingV1Params, UserShowV1Params, UserLookupV1Params, TweetShowV1Params, TweetLookupNoMapV1Params, TweetLookupMapV1Params, TweetLookupMapV1Result, ListListsV1Params, ListV1, ListMembersV1Params, ListMemberShowV1Params, ListMembershipsV1Params, ListOwnershipsV1Params, GetListV1Params, ListStatusesV1Params, ListSubscriptionsV1Params } from '../types';
import { HomeTimelineV1Paginator, ListTimelineV1Paginator, MentionTimelineV1Paginator, UserTimelineV1Paginator } from '../paginators/tweet.paginator.v1';
import { MuteUserIdsV1Paginator, MuteUserListV1Paginator } from '../paginators/mutes.paginator.v1';
import { FriendshipsIncomingV1Paginator, FriendshipsOutgoingV1Paginator, UserSearchV1Paginator } from '../paginators/user.paginator.v1';
import { ListMembershipsV1Paginator, ListMembersV1Paginator, ListOwnershipsV1Paginator, ListSubscribersV1Paginator, ListSubscriptionsV1Paginator } from '../paginators/list.paginator.v1';
import TweetStream from '../stream/TweetStream';
import { PromiseOrType } from '../types/shared.types';
/**
 * Base Twitter v1 client with only read right.
 */
export default class TwitterApiv1ReadOnly extends TwitterApiSubClient {
    protected _prefix: string;
    /**
     * Returns a single Tweet, specified by the id parameter. The Tweet's author will also be embedded within the Tweet.
     * https://developer.twitter.com/en/docs/twitter-api/v1/tweets/post-and-engage/api-reference/get-statuses-show-id
     */
    singleTweet(tweetId: string, options?: Partial<TweetShowV1Params>): Promise<TweetV1>;
    /**
     * Returns fully-hydrated Tweet objects for up to 100 Tweets per request.
     * https://developer.twitter.com/en/docs/twitter-api/v1/tweets/post-and-engage/api-reference/get-statuses-lookup
     */
    tweets(ids: string | string[], options?: TweetLookupNoMapV1Params): Promise<TweetV1[]>;
    tweets(ids: string | string[], options: TweetLookupMapV1Params): Promise<TweetLookupMapV1Result>;
    /**
     * Returns a single Tweet, specified by either a Tweet web URL or the Tweet ID, in an oEmbed-compatible format.
     * The returned HTML snippet will be automatically recognized as an Embedded Tweet when Twitter's widget JavaScript is included on the page.
     * https://developer.twitter.com/en/docs/twitter-api/v1/tweets/post-and-engage/api-reference/get-statuses-oembed
     */
    oembedTweet(tweetId: string, options?: Partial<OembedTweetV1Params>): Promise<OembedTweetV1Result>;
    /**
     * Returns a collection of the most recent Tweets and Retweets posted by the authenticating user and the users they follow.
     * The home timeline is central to how most users interact with the Twitter service.
     * https://developer.twitter.com/en/docs/twitter-api/v1/tweets/timelines/api-reference/get-statuses-home_timeline
     */
    homeTimeline(options?: Partial<TweetV1TimelineParams>): Promise<HomeTimelineV1Paginator>;
    /**
     * Returns the 20 most recent mentions (Tweets containing a users's @screen_name) for the authenticating user.
     * The timeline returned is the equivalent of the one seen when you view your mentions on twitter.com.
     * https://developer.twitter.com/en/docs/twitter-api/v1/tweets/timelines/api-reference/get-statuses-mentions_timeline
     */
    mentionTimeline(options?: Partial<TweetV1TimelineParams>): Promise<MentionTimelineV1Paginator>;
    /**
     * Returns a collection of the most recent Tweets posted by the user indicated by the user_id parameters.
     * User timelines belonging to protected users may only be requested when the authenticated user either "owns" the timeline or is an approved follower of the owner.
     * https://developer.twitter.com/en/docs/twitter-api/v1/tweets/timelines/api-reference/get-statuses-user_timeline
     */
    userTimeline(userId: string, options?: Partial<TweetV1UserTimelineParams>): Promise<UserTimelineV1Paginator>;
    /**
     * Returns a collection of the most recent Tweets posted by the user indicated by the screen_name parameters.
     * User timelines belonging to protected users may only be requested when the authenticated user either "owns" the timeline or is an approved follower of the owner.
     * https://developer.twitter.com/en/docs/twitter-api/v1/tweets/timelines/api-reference/get-statuses-user_timeline
     */
    userTimelineByUsername(username: string, options?: Partial<TweetV1UserTimelineParams>): Promise<UserTimelineV1Paginator>;
    /**
     * Returns a variety of information about the user specified by the required user_id or screen_name parameter.
     * The author's most recent Tweet will be returned inline when possible.
     * https://developer.twitter.com/en/docs/twitter-api/v1/accounts-and-users/follow-search-get-users/api-reference/get-users-show
     */
    user(user: UserShowV1Params): Promise<UserV1>;
    /**
     * Returns fully-hydrated user objects for up to 100 users per request,
     * as specified by comma-separated values passed to the user_id and/or screen_name parameters.
     * https://developer.twitter.com/en/docs/twitter-api/v1/accounts-and-users/follow-search-get-users/api-reference/get-users-lookup
     */
    users(query: UserLookupV1Params): Promise<UserV1[]>;
    /**
     * Returns an HTTP 200 OK response code and a representation of the requesting user if authentication was successful;
     * returns a 401 status code and an error message if not.
     * Use this method to test if supplied user credentials are valid.
     * https://developer.twitter.com/en/docs/twitter-api/v1/accounts-and-users/manage-account-settings/api-reference/get-account-verify_credentials
     */
    verifyCredentials(options?: Partial<VerifyCredentialsV1Params>): Promise<UserV1>;
    /**
     * Returns an array of user objects the authenticating user has muted.
     * https://developer.twitter.com/en/docs/twitter-api/v1/accounts-and-users/mute-block-report-users/api-reference/get-mutes-users-list
     */
    listMutedUsers(options?: Partial<MuteUserListV1Params>): Promise<MuteUserListV1Paginator>;
    /**
     * Returns an array of numeric user ids the authenticating user has muted.
     * https://developer.twitter.com/en/docs/twitter-api/v1/accounts-and-users/mute-block-report-users/api-reference/get-mutes-users-ids
     */
    listMutedUserIds(options?: Partial<MuteUserIdsV1Params>): Promise<MuteUserIdsV1Paginator>;
    /**
     * Provides a simple, relevance-based search interface to public user accounts on Twitter.
     * https://developer.twitter.com/en/docs/twitter-api/v1/accounts-and-users/follow-search-get-users/api-reference/get-users-search
     */
    searchUsers(query: string, options?: Partial<UserSearchV1Params>): Promise<UserSearchV1Paginator>;
    /**
     * Returns detailed information about the relationship between two arbitrary users.
     * https://developer.twitter.com/en/docs/twitter-api/v1/accounts-and-users/follow-search-get-users/api-reference/get-friendships-show
     */
    friendship(sources: FriendshipShowV1Params): Promise<FriendshipV1>;
    /**
     * Returns the relationships of the authenticating user to the comma-separated list of up to 100 screen_names or user_ids provided.
     * https://developer.twitter.com/en/docs/twitter-api/v1/accounts-and-users/follow-search-get-users/api-reference/get-friendships-lookup
     */
    friendships(friendships: FriendshipLookupV1Params): Promise<FriendshipLookupV1[]>;
    /**
     * Returns a collection of user_ids that the currently authenticated user does not want to receive retweets from.
     * https://developer.twitter.com/en/docs/twitter-api/v1/accounts-and-users/follow-search-get-users/api-reference/get-friendships-no_retweets-ids
     */
    friendshipsNoRetweets(): Promise<string[]>;
    /**
     * Returns a collection of numeric IDs for every user who has a pending request to follow the authenticating user.
     * https://developer.twitter.com/en/docs/twitter-api/v1/accounts-and-users/follow-search-get-users/api-reference/get-friendships-incoming
     */
    friendshipsIncoming(options?: Partial<FriendshipsIncomingV1Params>): Promise<FriendshipsIncomingV1Paginator>;
    /**
     * Returns a collection of numeric IDs for every protected user for whom the authenticating user has a pending follow request.
     * https://developer.twitter.com/en/docs/twitter-api/v1/accounts-and-users/follow-search-get-users/api-reference/get-friendships-outgoing
     */
    friendshipsOutgoing(options?: Partial<FriendshipsIncomingV1Params>): Promise<FriendshipsOutgoingV1Paginator>;
    /**
     * Get current account settings for authenticating user.
     * https://developer.twitter.com/en/docs/twitter-api/v1/accounts-and-users/manage-account-settings/api-reference/get-account-settings
     */
    accountSettings(): Promise<AccountSettingsV1>;
    /**
     * Returns a map of the available size variations of the specified user's profile banner.
     * If the user has not uploaded a profile banner, a HTTP 404 will be served instead.
     * https://developer.twitter.com/en/docs/twitter-api/v1/accounts-and-users/manage-account-settings/api-reference/get-users-profile_banner
     */
    userProfileBannerSizes(params: ProfileBannerSizeV1Params): Promise<ProfileBannerSizeV1>;
    /**
     * Returns the specified list. Private lists will only be shown if the authenticated user owns the specified list.
     * https://developer.twitter.com/en/docs/twitter-api/v1/accounts-and-users/create-manage-lists/api-reference/get-lists-show
     */
    list(options: GetListV1Params): Promise<ListV1>;
    /**
     * Returns all lists the authenticating or specified user subscribes to, including their own.
     * If no user is given, the authenticating user is used.
     * https://developer.twitter.com/en/docs/twitter-api/v1/accounts-and-users/create-manage-lists/api-reference/get-lists-list
     */
    lists(options?: ListListsV1Params): Promise<ListV1[]>;
    /**
     * Returns the members of the specified list. Private list members will only be shown if the authenticated user owns the specified list.
     * https://developer.twitter.com/en/docs/twitter-api/v1/accounts-and-users/create-manage-lists/api-reference/get-lists-members
     */
    listMembers(options?: Partial<ListMembersV1Params>): Promise<ListMembersV1Paginator>;
    /**
     * Check if the specified user is a member of the specified list.
     * https://developer.twitter.com/en/docs/twitter-api/v1/accounts-and-users/create-manage-lists/api-reference/get-lists-members-show
     */
    listGetMember(options: ListMemberShowV1Params): Promise<UserV1>;
    /**
     * Returns the lists the specified user has been added to.
     * If user_id or screen_name are not provided, the memberships for the authenticating user are returned.
     * https://developer.twitter.com/en/docs/twitter-api/v1/accounts-and-users/create-manage-lists/api-reference/get-lists-memberships
     */
    listMemberships(options?: Partial<ListMembershipsV1Params>): Promise<ListMembershipsV1Paginator>;
    /**
     * Returns the lists owned by the specified Twitter user. Private lists will only be shown if the authenticated user is also the owner of the lists.
     * https://developer.twitter.com/en/docs/twitter-api/v1/accounts-and-users/create-manage-lists/api-reference/get-lists-ownerships
     */
    listOwnerships(options?: Partial<ListOwnershipsV1Params>): Promise<ListOwnershipsV1Paginator>;
    /**
     * Returns a timeline of tweets authored by members of the specified list. Retweets are included by default.
     * https://developer.twitter.com/en/docs/twitter-api/v1/accounts-and-users/create-manage-lists/api-reference/get-lists-statuses
     */
    listStatuses(options: Partial<ListStatusesV1Params>): Promise<ListTimelineV1Paginator>;
    /**
     * Returns the subscribers of the specified list. Private list subscribers will only be shown if the authenticated user owns the specified list.
     * https://developer.twitter.com/en/docs/twitter-api/v1/accounts-and-users/create-manage-lists/api-reference/get-lists-subscribers
     */
    listSubscribers(options?: Partial<ListMembersV1Params>): Promise<ListSubscribersV1Paginator>;
    /**
     * Check if the specified user is a subscriber of the specified list. Returns the user if they are a subscriber.
     * https://developer.twitter.com/en/docs/twitter-api/v1/accounts-and-users/create-manage-lists/api-reference/get-lists-subscribers-show
     */
    listGetSubscriber(options: ListMemberShowV1Params): Promise<UserV1>;
    /**
     * Obtain a collection of the lists the specified user is subscribed to, 20 lists per page by default.
     * Does not include the user's own lists.
     * https://developer.twitter.com/en/docs/twitter-api/v1/accounts-and-users/create-manage-lists/api-reference/get-lists-subscriptions
     */
    listSubscriptions(options?: Partial<ListSubscriptionsV1Params>): Promise<ListSubscriptionsV1Paginator>;
    /**
     * The STATUS command (this method) is used to periodically poll for updates of media processing operation.
     * After the STATUS command response returns succeeded, you can move on to the next step which is usually create Tweet with media_id.
     * https://developer.twitter.com/en/docs/twitter-api/v1/media/upload-media/api-reference/get-media-upload-status
     */
    mediaInfo(mediaId: string): Promise<MediaStatusV1Result>;
    /**
     * Returns public statuses that match one or more filter predicates.
     * Multiple parameters may be specified which allows most clients to use a single connection to the Streaming API.
     * https://developer.twitter.com/en/docs/twitter-api/v1/tweets/filter-realtime/api-reference/post-statuses-filter
     */
    filterStream(params?: Partial<FilterStreamV1Params> & {
        autoConnect?: true;
    }): Promise<TweetStream<TweetV1>>;
    filterStream(params: Partial<FilterStreamV1Params> & {
        autoConnect: false;
    }): TweetStream<TweetV1>;
    filterStream(params?: Partial<FilterStreamV1Params> & {
        autoConnect?: boolean;
    }): PromiseOrType<TweetStream<TweetV1>>;
    /**
     * Returns a small random sample of all public statuses.
     * The Tweets returned by the default access level are the same, so if two different clients connect to this endpoint, they will see the same Tweets.
     * https://developer.twitter.com/en/docs/twitter-api/v1/tweets/sample-realtime/api-reference/get-statuses-sample
     */
    sampleStream(params?: Partial<SampleStreamV1Params> & {
        autoConnect?: true;
    }): Promise<TweetStream<TweetV1>>;
    sampleStream(params: Partial<SampleStreamV1Params> & {
        autoConnect: false;
    }): TweetStream<TweetV1>;
    sampleStream(params?: Partial<SampleStreamV1Params> & {
        autoConnect?: boolean;
    }): PromiseOrType<TweetStream<TweetV1>>;
    /**
     * Create a client that is prefixed with `https//stream.twitter.com` instead of classic API URL.
     */
    get stream(): this;
    /**
     * Returns the top 50 trending topics for a specific id, if trending information is available for it.
     * Note: The id parameter for this endpoint is the "where on earth identifier" or WOEID, which is a legacy identifier created by Yahoo and has been deprecated.
     * https://developer.twitter.com/en/docs/twitter-api/v1/trends/trends-for-location/api-reference/get-trends-place
     */
    trendsByPlace(woeId: string | number, options?: Partial<TrendsPlaceV1Params>): Promise<TrendMatchV1[]>;
    /**
     * Returns the locations that Twitter has trending topic information for.
     * The response is an array of "locations" that encode the location's WOEID
     * and some other human-readable information such as a canonical name and country the location belongs in.
     * https://developer.twitter.com/en/docs/twitter-api/v1/trends/locations-with-trending-topics/api-reference/get-trends-available
     */
    trendsAvailable(): Promise<TrendLocationV1[]>;
    /**
     * Returns the locations that Twitter has trending topic information for, closest to a specified location.
     * https://developer.twitter.com/en/docs/twitter-api/v1/trends/locations-with-trending-topics/api-reference/get-trends-closest
     */
    trendsClosest(lat: number, long: number): Promise<TrendLocationV1[]>;
    /**
     * Returns all the information about a known place.
     * https://developer.twitter.com/en/docs/twitter-api/v1/geo/place-information/api-reference/get-geo-id-place_id
     */
    geoPlace(placeId: string): Promise<PlaceV1>;
    /**
     * Search for places that can be attached to a Tweet via POST statuses/update.
     * This request will return a list of all the valid places that can be used as the place_id when updating a status.
     * https://developer.twitter.com/en/docs/twitter-api/v1/geo/places-near-location/api-reference/get-geo-search
     */
    geoSearch(options: Partial<SearchGeoV1Params>): Promise<SearchGeoV1Result>;
    /**
     * Given a latitude and a longitude, searches for up to 20 places that can be used as a place_id when updating a status.
     * This request is an informative call and will deliver generalized results about geography.
     * https://developer.twitter.com/en/docs/twitter-api/v1/geo/places-near-location/api-reference/get-geo-reverse_geocode
     */
    geoReverseGeoCode(options: ReverseGeoCodeV1Params): Promise<ReverseGeoCodeV1Result>;
    /**
     * Returns the current rate limits for methods belonging to the specified resource families.
     * Each API resource belongs to a "resource family" which is indicated in its method documentation.
     * The method's resource family can be determined from the first component of the path after the resource version.
     * https://developer.twitter.com/en/docs/twitter-api/v1/developer-utilities/rate-limit-status/api-reference/get-application-rate_limit_status
     */
    rateLimitStatuses(...resources: TAppRateLimitResourceV1[]): Promise<AppRateLimitV1Result>;
    /**
     * Returns the list of languages supported by Twitter along with the language code supported by Twitter.
     * https://developer.twitter.com/en/docs/twitter-api/v1/developer-utilities/supported-languages/api-reference/get-help-languages
     */
    supportedLanguages(): Promise<HelpLanguageV1Result[]>;
}
