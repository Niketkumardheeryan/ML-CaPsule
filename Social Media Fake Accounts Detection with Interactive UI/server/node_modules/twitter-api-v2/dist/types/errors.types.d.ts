/// <reference types="node" />
import type { TwitterRateLimit, TwitterResponse } from '../types';
import type { ClientRequest, IncomingMessage, IncomingHttpHeaders } from 'http';
export interface ErrorV1 {
    code: number;
    message: string;
}
/** Errors included in response payload with a OK HTTP status (code ~= 200) */
export interface InlineErrorV2 {
    value?: string;
    detail: string;
    title: string;
    resource_type?: string;
    parameter?: string;
    resource_id?: string;
    reason?: string;
    type: string;
}
/** Error payload thrown when HTTP code is not OK */
export interface ErrorV2 {
    detail: string;
    title: string;
    type: string;
    errors: {
        message: string;
        parameters?: {
            [parameterName: string]: string[];
        };
    }[];
}
export declare type TRequestError = TwitterApiRequestError | TwitterApiError;
export interface TwitterErrorPayload<T = any> {
    request: ClientRequest;
    rawResponse?: IncomingMessage;
    response?: TwitterResponse<T>;
    error?: Error;
}
export interface TwitterApiErrorData {
    errors: (ErrorV1 | ErrorV2)[];
    title?: string;
    detail?: string;
    type?: string;
}
export declare enum ETwitterApiError {
    Request = "request",
    PartialResponse = "partial-response",
    Response = "response"
}
export interface TwitterApiRequestError {
    type: ETwitterApiError.Request;
    error: true;
    readonly requestError: Error;
}
export interface TwitterApiError extends TwitterResponse<TwitterApiErrorData> {
    type: ETwitterApiError.Response;
    error: true;
    /** HTTP status code */
    code: number;
}
declare abstract class ApiError extends Error {
    abstract type: ETwitterApiError.Request | ETwitterApiError.Response | ETwitterApiError.PartialResponse;
    abstract request: ClientRequest;
    error: true;
}
interface IBuildApiRequestError {
    readonly request: ClientRequest;
    error: Error;
}
export declare class ApiRequestError extends ApiError implements TwitterApiRequestError {
    protected _options: any;
    type: ETwitterApiError.Request;
    constructor(message: string, options: IBuildApiRequestError);
    get request(): ClientRequest;
    get requestError(): Error;
    toJSON(): {
        type: ETwitterApiError.Request;
        error: Error;
    };
}
interface IBuildApiPartialRequestError {
    readonly request: ClientRequest;
    readonly response: IncomingMessage;
    readonly rawContent: string;
    responseError: Error;
}
export declare class ApiPartialResponseError extends ApiError implements IBuildApiPartialRequestError {
    protected _options: any;
    type: ETwitterApiError.PartialResponse;
    constructor(message: string, options: IBuildApiPartialRequestError);
    get request(): ClientRequest;
    get response(): IncomingMessage;
    get responseError(): Error;
    get rawContent(): string;
    toJSON(): {
        type: ETwitterApiError.PartialResponse;
        error: Error;
    };
}
interface IBuildApiResponseError {
    code: number;
    request: ClientRequest;
    response: IncomingMessage;
    headers: IncomingHttpHeaders;
    data: TwitterApiErrorData;
    rateLimit?: TwitterRateLimit;
}
export declare class ApiResponseError extends ApiError implements TwitterApiError, IBuildApiResponseError {
    protected _options: any;
    type: ETwitterApiError.Response;
    /** HTTP error code */
    code: number;
    headers: IncomingHttpHeaders;
    data: TwitterApiErrorData;
    rateLimit?: TwitterRateLimit;
    constructor(message: string, options: IBuildApiResponseError);
    get request(): ClientRequest;
    get response(): IncomingMessage;
    /** Check for presence of one of given v1/v2 error codes. */
    hasErrorCode(...codes: (EApiV1ErrorCode | number)[] | (EApiV2ErrorCode | string)[]): boolean;
    get errors(): (ErrorV1 | ErrorV2)[] | undefined;
    get rateLimitError(): boolean;
    get isAuthError(): boolean;
    toJSON(): {
        type: ETwitterApiError.Response;
        code: number;
        error: TwitterApiErrorData;
        rateLimit: TwitterRateLimit | undefined;
        headers: IncomingHttpHeaders;
    };
}
export declare enum EApiV1ErrorCode {
    InvalidCoordinates = 3,
    NoLocationFound = 13,
    AuthenticationFail = 32,
    InvalidOrExpiredToken = 89,
    UnableToVerifyCredentials = 99,
    AuthTimestampInvalid = 135,
    BadAuthenticationData = 215,
    NoUserMatch = 17,
    UserNotFound = 50,
    ResourceNotFound = 34,
    TweetNotFound = 144,
    TweetNotVisible = 179,
    NotAllowedResource = 220,
    MediaIdNotFound = 325,
    TweetNoLongerAvailable = 421,
    TweetViolatedRules = 422,
    TargetUserSuspended = 63,
    YouAreSuspended = 64,
    AccountUpdateFailed = 120,
    NoSelfSpamReport = 36,
    NoSelfMute = 271,
    AccountLocked = 326,
    RateLimitExceeded = 88,
    NoDMRightForApp = 93,
    OverCapacity = 130,
    InternalError = 131,
    TooManyFollowings = 161,
    TweetLimitExceeded = 185,
    DuplicatedTweet = 187,
    TooManySpamReports = 205,
    RequestLooksLikeSpam = 226,
    NoWriteRightForApp = 261,
    TweetActionsDisabled = 425,
    TweetRepliesRestricted = 433,
    NamedParameterMissing = 38,
    InvalidAttachmentUrl = 44,
    TweetTextTooLong = 186,
    MissingUrlParameter = 195,
    NoMultipleGifs = 323,
    InvalidMediaIds = 324,
    InvalidUrl = 407,
    TooManyTweetAttachments = 386,
    StatusAlreadyFavorited = 139,
    FollowRequestAlreadySent = 160,
    CannotUnmuteANonMutedAccount = 272,
    TweetAlreadyRetweeted = 327,
    ReplyToDeletedTweet = 385,
    DMReceiverNotFollowingYou = 150,
    UnableToSendDM = 151,
    MustAllowDMFromAnyone = 214,
    CannotSendDMToThisUser = 349,
    DMTextTooLong = 354,
    SubscriptionAlreadyExists = 355,
    CallbackUrlNotApproved = 415,
    SuspendedApplication = 416,
    OobOauthIsNotAllowed = 417
}
export declare enum EApiV2ErrorCode {
    InvalidRequest = "https://api.twitter.com/2/problems/invalid-request",
    ClientForbidden = "https://api.twitter.com/2/problems/client-forbidden",
    UnsupportedAuthentication = "https://api.twitter.com/2/problems/unsupported-authentication",
    InvalidRules = "https://api.twitter.com/2/problems/invalid-rules",
    TooManyRules = "https://api.twitter.com/2/problems/rule-cap",
    DuplicatedRules = "https://api.twitter.com/2/problems/duplicate-rules",
    RateLimitExceeded = "https://api.twitter.com/2/problems/usage-capped",
    ConnectionError = "https://api.twitter.com/2/problems/streaming-connection",
    ClientDisconnected = "https://api.twitter.com/2/problems/client-disconnected",
    TwitterDisconnectedYou = "https://api.twitter.com/2/problems/operational-disconnect",
    ResourceNotFound = "https://api.twitter.com/2/problems/resource-not-found",
    ResourceUnauthorized = "https://api.twitter.com/2/problems/not-authorized-for-resource",
    DisallowedResource = "https://api.twitter.com/2/problems/disallowed-resource"
}
export {};
