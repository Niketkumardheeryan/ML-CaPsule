"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.EApiV2ErrorCode = exports.EApiV1ErrorCode = exports.ApiResponseError = exports.ApiPartialResponseError = exports.ApiRequestError = exports.ETwitterApiError = void 0;
var ETwitterApiError;
(function (ETwitterApiError) {
    ETwitterApiError["Request"] = "request";
    ETwitterApiError["PartialResponse"] = "partial-response";
    ETwitterApiError["Response"] = "response";
})(ETwitterApiError = exports.ETwitterApiError || (exports.ETwitterApiError = {}));
/* ERRORS INSTANCES */
class ApiError extends Error {
    constructor() {
        super(...arguments);
        this.error = true;
    }
}
class ApiRequestError extends ApiError {
    constructor(message, options) {
        super(message);
        this.type = ETwitterApiError.Request;
        Error.captureStackTrace(this, this.constructor);
        // Do not show on Node stack trace
        Object.defineProperty(this, '_options', { value: options });
    }
    get request() {
        return this._options.request;
    }
    get requestError() {
        return this._options.requestError;
    }
    toJSON() {
        return {
            type: this.type,
            error: this.requestError,
        };
    }
}
exports.ApiRequestError = ApiRequestError;
class ApiPartialResponseError extends ApiError {
    constructor(message, options) {
        super(message);
        this.type = ETwitterApiError.PartialResponse;
        Error.captureStackTrace(this, this.constructor);
        // Do not show on Node stack trace
        Object.defineProperty(this, '_options', { value: options });
    }
    get request() {
        return this._options.request;
    }
    get response() {
        return this._options.response;
    }
    get responseError() {
        return this._options.responseError;
    }
    get rawContent() {
        return this._options.rawContent;
    }
    toJSON() {
        return {
            type: this.type,
            error: this.responseError,
        };
    }
}
exports.ApiPartialResponseError = ApiPartialResponseError;
class ApiResponseError extends ApiError {
    constructor(message, options) {
        super(message);
        this.type = ETwitterApiError.Response;
        Error.captureStackTrace(this, this.constructor);
        // Do not show on Node stack trace
        Object.defineProperty(this, '_options', { value: options });
        this.code = options.code;
        this.headers = options.headers;
        this.rateLimit = options.rateLimit;
        this.data = options.data;
    }
    get request() {
        return this._options.request;
    }
    get response() {
        return this._options.response;
    }
    /** Check for presence of one of given v1/v2 error codes. */
    hasErrorCode(...codes) {
        const errors = this.errors;
        // No errors
        if (!(errors === null || errors === void 0 ? void 0 : errors.length)) {
            return false;
        }
        // v1 errors
        if ('code' in errors[0]) {
            const v1errors = errors;
            return v1errors.some(error => codes.includes(error.code));
        }
        // v2 error
        const v2error = this.data;
        return codes.includes(v2error.type);
    }
    get errors() {
        var _a;
        return (_a = this.data) === null || _a === void 0 ? void 0 : _a.errors;
    }
    get rateLimitError() {
        return this.code === 420 || this.code === 429;
    }
    get isAuthError() {
        if (this.code === 401) {
            return true;
        }
        return this.hasErrorCode(EApiV1ErrorCode.AuthTimestampInvalid, EApiV1ErrorCode.AuthenticationFail, EApiV1ErrorCode.BadAuthenticationData, EApiV1ErrorCode.InvalidOrExpiredToken);
    }
    toJSON() {
        return {
            type: this.type,
            code: this.code,
            error: this.data,
            rateLimit: this.rateLimit,
            headers: this.headers,
        };
    }
}
exports.ApiResponseError = ApiResponseError;
var EApiV1ErrorCode;
(function (EApiV1ErrorCode) {
    // Location errors
    EApiV1ErrorCode[EApiV1ErrorCode["InvalidCoordinates"] = 3] = "InvalidCoordinates";
    EApiV1ErrorCode[EApiV1ErrorCode["NoLocationFound"] = 13] = "NoLocationFound";
    // Authentication failures
    EApiV1ErrorCode[EApiV1ErrorCode["AuthenticationFail"] = 32] = "AuthenticationFail";
    EApiV1ErrorCode[EApiV1ErrorCode["InvalidOrExpiredToken"] = 89] = "InvalidOrExpiredToken";
    EApiV1ErrorCode[EApiV1ErrorCode["UnableToVerifyCredentials"] = 99] = "UnableToVerifyCredentials";
    EApiV1ErrorCode[EApiV1ErrorCode["AuthTimestampInvalid"] = 135] = "AuthTimestampInvalid";
    EApiV1ErrorCode[EApiV1ErrorCode["BadAuthenticationData"] = 215] = "BadAuthenticationData";
    // Resources not found or visible
    EApiV1ErrorCode[EApiV1ErrorCode["NoUserMatch"] = 17] = "NoUserMatch";
    EApiV1ErrorCode[EApiV1ErrorCode["UserNotFound"] = 50] = "UserNotFound";
    EApiV1ErrorCode[EApiV1ErrorCode["ResourceNotFound"] = 34] = "ResourceNotFound";
    EApiV1ErrorCode[EApiV1ErrorCode["TweetNotFound"] = 144] = "TweetNotFound";
    EApiV1ErrorCode[EApiV1ErrorCode["TweetNotVisible"] = 179] = "TweetNotVisible";
    EApiV1ErrorCode[EApiV1ErrorCode["NotAllowedResource"] = 220] = "NotAllowedResource";
    EApiV1ErrorCode[EApiV1ErrorCode["MediaIdNotFound"] = 325] = "MediaIdNotFound";
    EApiV1ErrorCode[EApiV1ErrorCode["TweetNoLongerAvailable"] = 421] = "TweetNoLongerAvailable";
    EApiV1ErrorCode[EApiV1ErrorCode["TweetViolatedRules"] = 422] = "TweetViolatedRules";
    // Account errors
    EApiV1ErrorCode[EApiV1ErrorCode["TargetUserSuspended"] = 63] = "TargetUserSuspended";
    EApiV1ErrorCode[EApiV1ErrorCode["YouAreSuspended"] = 64] = "YouAreSuspended";
    EApiV1ErrorCode[EApiV1ErrorCode["AccountUpdateFailed"] = 120] = "AccountUpdateFailed";
    EApiV1ErrorCode[EApiV1ErrorCode["NoSelfSpamReport"] = 36] = "NoSelfSpamReport";
    EApiV1ErrorCode[EApiV1ErrorCode["NoSelfMute"] = 271] = "NoSelfMute";
    EApiV1ErrorCode[EApiV1ErrorCode["AccountLocked"] = 326] = "AccountLocked";
    // Application live errors / Twitter errors
    EApiV1ErrorCode[EApiV1ErrorCode["RateLimitExceeded"] = 88] = "RateLimitExceeded";
    EApiV1ErrorCode[EApiV1ErrorCode["NoDMRightForApp"] = 93] = "NoDMRightForApp";
    EApiV1ErrorCode[EApiV1ErrorCode["OverCapacity"] = 130] = "OverCapacity";
    EApiV1ErrorCode[EApiV1ErrorCode["InternalError"] = 131] = "InternalError";
    EApiV1ErrorCode[EApiV1ErrorCode["TooManyFollowings"] = 161] = "TooManyFollowings";
    EApiV1ErrorCode[EApiV1ErrorCode["TweetLimitExceeded"] = 185] = "TweetLimitExceeded";
    EApiV1ErrorCode[EApiV1ErrorCode["DuplicatedTweet"] = 187] = "DuplicatedTweet";
    EApiV1ErrorCode[EApiV1ErrorCode["TooManySpamReports"] = 205] = "TooManySpamReports";
    EApiV1ErrorCode[EApiV1ErrorCode["RequestLooksLikeSpam"] = 226] = "RequestLooksLikeSpam";
    EApiV1ErrorCode[EApiV1ErrorCode["NoWriteRightForApp"] = 261] = "NoWriteRightForApp";
    EApiV1ErrorCode[EApiV1ErrorCode["TweetActionsDisabled"] = 425] = "TweetActionsDisabled";
    EApiV1ErrorCode[EApiV1ErrorCode["TweetRepliesRestricted"] = 433] = "TweetRepliesRestricted";
    // Invalid request parameters
    EApiV1ErrorCode[EApiV1ErrorCode["NamedParameterMissing"] = 38] = "NamedParameterMissing";
    EApiV1ErrorCode[EApiV1ErrorCode["InvalidAttachmentUrl"] = 44] = "InvalidAttachmentUrl";
    EApiV1ErrorCode[EApiV1ErrorCode["TweetTextTooLong"] = 186] = "TweetTextTooLong";
    EApiV1ErrorCode[EApiV1ErrorCode["MissingUrlParameter"] = 195] = "MissingUrlParameter";
    EApiV1ErrorCode[EApiV1ErrorCode["NoMultipleGifs"] = 323] = "NoMultipleGifs";
    EApiV1ErrorCode[EApiV1ErrorCode["InvalidMediaIds"] = 324] = "InvalidMediaIds";
    EApiV1ErrorCode[EApiV1ErrorCode["InvalidUrl"] = 407] = "InvalidUrl";
    EApiV1ErrorCode[EApiV1ErrorCode["TooManyTweetAttachments"] = 386] = "TooManyTweetAttachments";
    // Already sent/deleted item
    EApiV1ErrorCode[EApiV1ErrorCode["StatusAlreadyFavorited"] = 139] = "StatusAlreadyFavorited";
    EApiV1ErrorCode[EApiV1ErrorCode["FollowRequestAlreadySent"] = 160] = "FollowRequestAlreadySent";
    EApiV1ErrorCode[EApiV1ErrorCode["CannotUnmuteANonMutedAccount"] = 272] = "CannotUnmuteANonMutedAccount";
    EApiV1ErrorCode[EApiV1ErrorCode["TweetAlreadyRetweeted"] = 327] = "TweetAlreadyRetweeted";
    EApiV1ErrorCode[EApiV1ErrorCode["ReplyToDeletedTweet"] = 385] = "ReplyToDeletedTweet";
    // DM Errors
    EApiV1ErrorCode[EApiV1ErrorCode["DMReceiverNotFollowingYou"] = 150] = "DMReceiverNotFollowingYou";
    EApiV1ErrorCode[EApiV1ErrorCode["UnableToSendDM"] = 151] = "UnableToSendDM";
    EApiV1ErrorCode[EApiV1ErrorCode["MustAllowDMFromAnyone"] = 214] = "MustAllowDMFromAnyone";
    EApiV1ErrorCode[EApiV1ErrorCode["CannotSendDMToThisUser"] = 349] = "CannotSendDMToThisUser";
    EApiV1ErrorCode[EApiV1ErrorCode["DMTextTooLong"] = 354] = "DMTextTooLong";
    // Appication misconfiguration
    EApiV1ErrorCode[EApiV1ErrorCode["SubscriptionAlreadyExists"] = 355] = "SubscriptionAlreadyExists";
    EApiV1ErrorCode[EApiV1ErrorCode["CallbackUrlNotApproved"] = 415] = "CallbackUrlNotApproved";
    EApiV1ErrorCode[EApiV1ErrorCode["SuspendedApplication"] = 416] = "SuspendedApplication";
    EApiV1ErrorCode[EApiV1ErrorCode["OobOauthIsNotAllowed"] = 417] = "OobOauthIsNotAllowed";
})(EApiV1ErrorCode = exports.EApiV1ErrorCode || (exports.EApiV1ErrorCode = {}));
var EApiV2ErrorCode;
(function (EApiV2ErrorCode) {
    // Request errors
    EApiV2ErrorCode["InvalidRequest"] = "https://api.twitter.com/2/problems/invalid-request";
    EApiV2ErrorCode["ClientForbidden"] = "https://api.twitter.com/2/problems/client-forbidden";
    EApiV2ErrorCode["UnsupportedAuthentication"] = "https://api.twitter.com/2/problems/unsupported-authentication";
    // Stream rules errors
    EApiV2ErrorCode["InvalidRules"] = "https://api.twitter.com/2/problems/invalid-rules";
    EApiV2ErrorCode["TooManyRules"] = "https://api.twitter.com/2/problems/rule-cap";
    EApiV2ErrorCode["DuplicatedRules"] = "https://api.twitter.com/2/problems/duplicate-rules";
    // Twitter errors
    EApiV2ErrorCode["RateLimitExceeded"] = "https://api.twitter.com/2/problems/usage-capped";
    EApiV2ErrorCode["ConnectionError"] = "https://api.twitter.com/2/problems/streaming-connection";
    EApiV2ErrorCode["ClientDisconnected"] = "https://api.twitter.com/2/problems/client-disconnected";
    EApiV2ErrorCode["TwitterDisconnectedYou"] = "https://api.twitter.com/2/problems/operational-disconnect";
    // Resource errors
    EApiV2ErrorCode["ResourceNotFound"] = "https://api.twitter.com/2/problems/resource-not-found";
    EApiV2ErrorCode["ResourceUnauthorized"] = "https://api.twitter.com/2/problems/not-authorized-for-resource";
    EApiV2ErrorCode["DisallowedResource"] = "https://api.twitter.com/2/problems/disallowed-resource";
})(EApiV2ErrorCode = exports.EApiV2ErrorCode || (exports.EApiV2ErrorCode = {}));
