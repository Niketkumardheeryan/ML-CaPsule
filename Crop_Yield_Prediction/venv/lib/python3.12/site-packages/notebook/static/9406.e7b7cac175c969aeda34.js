"use strict";
(self["webpackChunk_JUPYTERLAB_CORE_OUTPUT"] = self["webpackChunk_JUPYTERLAB_CORE_OUTPUT"] || []).push([[9406],{

/***/ 69406:
/***/ (function(__unused_webpack_module, exports, __webpack_require__) {


/* --------------------------------------------------------------------------------------------
 * Copyright (c) Microsoft Corporation. All rights reserved.
 * Licensed under the MIT License. See License.txt in the project root for license information.
 * ------------------------------------------------------------------------------------------ */
var __createBinding = (this && this.__createBinding) || (Object.create ? (function(o, m, k, k2) {
    if (k2 === undefined) k2 = k;
    var desc = Object.getOwnPropertyDescriptor(m, k);
    if (!desc || ("get" in desc ? !m.__esModule : desc.writable || desc.configurable)) {
      desc = { enumerable: true, get: function() { return m[k]; } };
    }
    Object.defineProperty(o, k2, desc);
}) : (function(o, m, k, k2) {
    if (k2 === undefined) k2 = k;
    o[k2] = m[k];
}));
var __exportStar = (this && this.__exportStar) || function(m, exports) {
    for (var p in m) if (p !== "default" && !Object.prototype.hasOwnProperty.call(exports, p)) __createBinding(exports, m, p);
};
Object.defineProperty(exports, "__esModule", ({ value: true }));
exports.createMessageConnection = exports.BrowserMessageWriter = exports.BrowserMessageReader = void 0;
const ril_1 = __webpack_require__(36028);
// Install the browser runtime abstract.
ril_1.default.install();
const api_1 = __webpack_require__(95748);
__exportStar(__webpack_require__(95748), exports);
class BrowserMessageReader extends api_1.AbstractMessageReader {
    constructor(port) {
        super();
        this._onData = new api_1.Emitter();
        this._messageListener = (event) => {
            this._onData.fire(event.data);
        };
        port.addEventListener('error', (event) => this.fireError(event));
        port.onmessage = this._messageListener;
    }
    listen(callback) {
        return this._onData.event(callback);
    }
}
exports.BrowserMessageReader = BrowserMessageReader;
class BrowserMessageWriter extends api_1.AbstractMessageWriter {
    constructor(port) {
        super();
        this.port = port;
        this.errorCount = 0;
        port.addEventListener('error', (event) => this.fireError(event));
    }
    write(msg) {
        try {
            this.port.postMessage(msg);
            return Promise.resolve();
        }
        catch (error) {
            this.handleError(error, msg);
            return Promise.reject(error);
        }
    }
    handleError(error, msg) {
        this.errorCount++;
        this.fireError(error, msg, this.errorCount);
    }
    end() {
    }
}
exports.BrowserMessageWriter = BrowserMessageWriter;
function createMessageConnection(reader, writer, logger, options) {
    if (logger === undefined) {
        logger = api_1.NullLogger;
    }
    if (api_1.ConnectionStrategy.is(options)) {
        options = { connectionStrategy: options };
    }
    return (0, api_1.createMessageConnection)(reader, writer, logger, options);
}
exports.createMessageConnection = createMessageConnection;


/***/ }),

/***/ 36028:
/***/ ((__unused_webpack_module, exports, __webpack_require__) => {


/* --------------------------------------------------------------------------------------------
 * Copyright (c) Microsoft Corporation. All rights reserved.
 * Licensed under the MIT License. See License.txt in the project root for license information.
 * ------------------------------------------------------------------------------------------ */
Object.defineProperty(exports, "__esModule", ({ value: true }));
const api_1 = __webpack_require__(95748);
class MessageBuffer extends api_1.AbstractMessageBuffer {
    constructor(encoding = 'utf-8') {
        super(encoding);
        this.asciiDecoder = new TextDecoder('ascii');
    }
    emptyBuffer() {
        return MessageBuffer.emptyBuffer;
    }
    fromString(value, _encoding) {
        return (new TextEncoder()).encode(value);
    }
    toString(value, encoding) {
        if (encoding === 'ascii') {
            return this.asciiDecoder.decode(value);
        }
        else {
            return (new TextDecoder(encoding)).decode(value);
        }
    }
    asNative(buffer, length) {
        if (length === undefined) {
            return buffer;
        }
        else {
            return buffer.slice(0, length);
        }
    }
    allocNative(length) {
        return new Uint8Array(length);
    }
}
MessageBuffer.emptyBuffer = new Uint8Array(0);
class ReadableStreamWrapper {
    constructor(socket) {
        this.socket = socket;
        this._onData = new api_1.Emitter();
        this._messageListener = (event) => {
            const blob = event.data;
            blob.arrayBuffer().then((buffer) => {
                this._onData.fire(new Uint8Array(buffer));
            }, () => {
                (0, api_1.RAL)().console.error(`Converting blob to array buffer failed.`);
            });
        };
        this.socket.addEventListener('message', this._messageListener);
    }
    onClose(listener) {
        this.socket.addEventListener('close', listener);
        return api_1.Disposable.create(() => this.socket.removeEventListener('close', listener));
    }
    onError(listener) {
        this.socket.addEventListener('error', listener);
        return api_1.Disposable.create(() => this.socket.removeEventListener('error', listener));
    }
    onEnd(listener) {
        this.socket.addEventListener('end', listener);
        return api_1.Disposable.create(() => this.socket.removeEventListener('end', listener));
    }
    onData(listener) {
        return this._onData.event(listener);
    }
}
class WritableStreamWrapper {
    constructor(socket) {
        this.socket = socket;
    }
    onClose(listener) {
        this.socket.addEventListener('close', listener);
        return api_1.Disposable.create(() => this.socket.removeEventListener('close', listener));
    }
    onError(listener) {
        this.socket.addEventListener('error', listener);
        return api_1.Disposable.create(() => this.socket.removeEventListener('error', listener));
    }
    onEnd(listener) {
        this.socket.addEventListener('end', listener);
        return api_1.Disposable.create(() => this.socket.removeEventListener('end', listener));
    }
    write(data, encoding) {
        if (typeof data === 'string') {
            if (encoding !== undefined && encoding !== 'utf-8') {
                throw new Error(`In a Browser environments only utf-8 text encoding is supported. But got encoding: ${encoding}`);
            }
            this.socket.send(data);
        }
        else {
            this.socket.send(data);
        }
        return Promise.resolve();
    }
    end() {
        this.socket.close();
    }
}
const _textEncoder = new TextEncoder();
const _ril = Object.freeze({
    messageBuffer: Object.freeze({
        create: (encoding) => new MessageBuffer(encoding)
    }),
    applicationJson: Object.freeze({
        encoder: Object.freeze({
            name: 'application/json',
            encode: (msg, options) => {
                if (options.charset !== 'utf-8') {
                    throw new Error(`In a Browser environments only utf-8 text encoding is supported. But got encoding: ${options.charset}`);
                }
                return Promise.resolve(_textEncoder.encode(JSON.stringify(msg, undefined, 0)));
            }
        }),
        decoder: Object.freeze({
            name: 'application/json',
            decode: (buffer, options) => {
                if (!(buffer instanceof Uint8Array)) {
                    throw new Error(`In a Browser environments only Uint8Arrays are supported.`);
                }
                return Promise.resolve(JSON.parse(new TextDecoder(options.charset).decode(buffer)));
            }
        })
    }),
    stream: Object.freeze({
        asReadableStream: (socket) => new ReadableStreamWrapper(socket),
        asWritableStream: (socket) => new WritableStreamWrapper(socket)
    }),
    console: console,
    timer: Object.freeze({
        setTimeout(callback, ms, ...args) {
            const handle = setTimeout(callback, ms, ...args);
            return { dispose: () => clearTimeout(handle) };
        },
        setImmediate(callback, ...args) {
            const handle = setTimeout(callback, 0, ...args);
            return { dispose: () => clearTimeout(handle) };
        },
        setInterval(callback, ms, ...args) {
            const handle = setInterval(callback, ms, ...args);
            return { dispose: () => clearInterval(handle) };
        },
    })
});
function RIL() {
    return _ril;
}
(function (RIL) {
    function install() {
        api_1.RAL.install(_ril);
    }
    RIL.install = install;
})(RIL || (RIL = {}));
exports["default"] = RIL;


/***/ }),

/***/ 95748:
/***/ ((__unused_webpack_module, exports, __webpack_require__) => {


/* --------------------------------------------------------------------------------------------
 * Copyright (c) Microsoft Corporation. All rights reserved.
 * Licensed under the MIT License. See License.txt in the project root for license information.
 * ------------------------------------------------------------------------------------------ */
/// <reference path="../../typings/thenable.d.ts" />
Object.defineProperty(exports, "__esModule", ({ value: true }));
exports.ProgressType = exports.ProgressToken = exports.createMessageConnection = exports.NullLogger = exports.ConnectionOptions = exports.ConnectionStrategy = exports.AbstractMessageBuffer = exports.WriteableStreamMessageWriter = exports.AbstractMessageWriter = exports.MessageWriter = exports.ReadableStreamMessageReader = exports.AbstractMessageReader = exports.MessageReader = exports.SharedArrayReceiverStrategy = exports.SharedArraySenderStrategy = exports.CancellationToken = exports.CancellationTokenSource = exports.Emitter = exports.Event = exports.Disposable = exports.LRUCache = exports.Touch = exports.LinkedMap = exports.ParameterStructures = exports.NotificationType9 = exports.NotificationType8 = exports.NotificationType7 = exports.NotificationType6 = exports.NotificationType5 = exports.NotificationType4 = exports.NotificationType3 = exports.NotificationType2 = exports.NotificationType1 = exports.NotificationType0 = exports.NotificationType = exports.ErrorCodes = exports.ResponseError = exports.RequestType9 = exports.RequestType8 = exports.RequestType7 = exports.RequestType6 = exports.RequestType5 = exports.RequestType4 = exports.RequestType3 = exports.RequestType2 = exports.RequestType1 = exports.RequestType0 = exports.RequestType = exports.Message = exports.RAL = void 0;
exports.MessageStrategy = exports.CancellationStrategy = exports.CancellationSenderStrategy = exports.CancellationReceiverStrategy = exports.ConnectionError = exports.ConnectionErrors = exports.LogTraceNotification = exports.SetTraceNotification = exports.TraceFormat = exports.TraceValues = exports.Trace = void 0;
const messages_1 = __webpack_require__(75285);
Object.defineProperty(exports, "Message", ({ enumerable: true, get: function () { return messages_1.Message; } }));
Object.defineProperty(exports, "RequestType", ({ enumerable: true, get: function () { return messages_1.RequestType; } }));
Object.defineProperty(exports, "RequestType0", ({ enumerable: true, get: function () { return messages_1.RequestType0; } }));
Object.defineProperty(exports, "RequestType1", ({ enumerable: true, get: function () { return messages_1.RequestType1; } }));
Object.defineProperty(exports, "RequestType2", ({ enumerable: true, get: function () { return messages_1.RequestType2; } }));
Object.defineProperty(exports, "RequestType3", ({ enumerable: true, get: function () { return messages_1.RequestType3; } }));
Object.defineProperty(exports, "RequestType4", ({ enumerable: true, get: function () { return messages_1.RequestType4; } }));
Object.defineProperty(exports, "RequestType5", ({ enumerable: true, get: function () { return messages_1.RequestType5; } }));
Object.defineProperty(exports, "RequestType6", ({ enumerable: true, get: function () { return messages_1.RequestType6; } }));
Object.defineProperty(exports, "RequestType7", ({ enumerable: true, get: function () { return messages_1.RequestType7; } }));
Object.defineProperty(exports, "RequestType8", ({ enumerable: true, get: function () { return messages_1.RequestType8; } }));
Object.defineProperty(exports, "RequestType9", ({ enumerable: true, get: function () { return messages_1.RequestType9; } }));
Object.defineProperty(exports, "ResponseError", ({ enumerable: true, get: function () { return messages_1.ResponseError; } }));
Object.defineProperty(exports, "ErrorCodes", ({ enumerable: true, get: function () { return messages_1.ErrorCodes; } }));
Object.defineProperty(exports, "NotificationType", ({ enumerable: true, get: function () { return messages_1.NotificationType; } }));
Object.defineProperty(exports, "NotificationType0", ({ enumerable: true, get: function () { return messages_1.NotificationType0; } }));
Object.defineProperty(exports, "NotificationType1", ({ enumerable: true, get: function () { return messages_1.NotificationType1; } }));
Object.defineProperty(exports, "NotificationType2", ({ enumerable: true, get: function () { return messages_1.NotificationType2; } }));
Object.defineProperty(exports, "NotificationType3", ({ enumerable: true, get: function () { return messages_1.NotificationType3; } }));
Object.defineProperty(exports, "NotificationType4", ({ enumerable: true, get: function () { return messages_1.NotificationType4; } }));
Object.defineProperty(exports, "NotificationType5", ({ enumerable: true, get: function () { return messages_1.NotificationType5; } }));
Object.defineProperty(exports, "NotificationType6", ({ enumerable: true, get: function () { return messages_1.NotificationType6; } }));
Object.defineProperty(exports, "NotificationType7", ({ enumerable: true, get: function () { return messages_1.NotificationType7; } }));
Object.defineProperty(exports, "NotificationType8", ({ enumerable: true, get: function () { return messages_1.NotificationType8; } }));
Object.defineProperty(exports, "NotificationType9", ({ enumerable: true, get: function () { return messages_1.NotificationType9; } }));
Object.defineProperty(exports, "ParameterStructures", ({ enumerable: true, get: function () { return messages_1.ParameterStructures; } }));
const linkedMap_1 = __webpack_require__(45164);
Object.defineProperty(exports, "LinkedMap", ({ enumerable: true, get: function () { return linkedMap_1.LinkedMap; } }));
Object.defineProperty(exports, "LRUCache", ({ enumerable: true, get: function () { return linkedMap_1.LRUCache; } }));
Object.defineProperty(exports, "Touch", ({ enumerable: true, get: function () { return linkedMap_1.Touch; } }));
const disposable_1 = __webpack_require__(68159);
Object.defineProperty(exports, "Disposable", ({ enumerable: true, get: function () { return disposable_1.Disposable; } }));
const events_1 = __webpack_require__(345);
Object.defineProperty(exports, "Event", ({ enumerable: true, get: function () { return events_1.Event; } }));
Object.defineProperty(exports, "Emitter", ({ enumerable: true, get: function () { return events_1.Emitter; } }));
const cancellation_1 = __webpack_require__(97770);
Object.defineProperty(exports, "CancellationTokenSource", ({ enumerable: true, get: function () { return cancellation_1.CancellationTokenSource; } }));
Object.defineProperty(exports, "CancellationToken", ({ enumerable: true, get: function () { return cancellation_1.CancellationToken; } }));
const sharedArrayCancellation_1 = __webpack_require__(50278);
Object.defineProperty(exports, "SharedArraySenderStrategy", ({ enumerable: true, get: function () { return sharedArrayCancellation_1.SharedArraySenderStrategy; } }));
Object.defineProperty(exports, "SharedArrayReceiverStrategy", ({ enumerable: true, get: function () { return sharedArrayCancellation_1.SharedArrayReceiverStrategy; } }));
const messageReader_1 = __webpack_require__(84806);
Object.defineProperty(exports, "MessageReader", ({ enumerable: true, get: function () { return messageReader_1.MessageReader; } }));
Object.defineProperty(exports, "AbstractMessageReader", ({ enumerable: true, get: function () { return messageReader_1.AbstractMessageReader; } }));
Object.defineProperty(exports, "ReadableStreamMessageReader", ({ enumerable: true, get: function () { return messageReader_1.ReadableStreamMessageReader; } }));
const messageWriter_1 = __webpack_require__(69248);
Object.defineProperty(exports, "MessageWriter", ({ enumerable: true, get: function () { return messageWriter_1.MessageWriter; } }));
Object.defineProperty(exports, "AbstractMessageWriter", ({ enumerable: true, get: function () { return messageWriter_1.AbstractMessageWriter; } }));
Object.defineProperty(exports, "WriteableStreamMessageWriter", ({ enumerable: true, get: function () { return messageWriter_1.WriteableStreamMessageWriter; } }));
const messageBuffer_1 = __webpack_require__(15506);
Object.defineProperty(exports, "AbstractMessageBuffer", ({ enumerable: true, get: function () { return messageBuffer_1.AbstractMessageBuffer; } }));
const connection_1 = __webpack_require__(6336);
Object.defineProperty(exports, "ConnectionStrategy", ({ enumerable: true, get: function () { return connection_1.ConnectionStrategy; } }));
Object.defineProperty(exports, "ConnectionOptions", ({ enumerable: true, get: function () { return connection_1.ConnectionOptions; } }));
Object.defineProperty(exports, "NullLogger", ({ enumerable: true, get: function () { return connection_1.NullLogger; } }));
Object.defineProperty(exports, "createMessageConnection", ({ enumerable: true, get: function () { return connection_1.createMessageConnection; } }));
Object.defineProperty(exports, "ProgressToken", ({ enumerable: true, get: function () { return connection_1.ProgressToken; } }));
Object.defineProperty(exports, "ProgressType", ({ enumerable: true, get: function () { return connection_1.ProgressType; } }));
Object.defineProperty(exports, "Trace", ({ enumerable: true, get: function () { return connection_1.Trace; } }));
Object.defineProperty(exports, "TraceValues", ({ enumerable: true, get: function () { return connection_1.TraceValues; } }));
Object.defineProperty(exports, "TraceFormat", ({ enumerable: true, get: function () { return connection_1.TraceFormat; } }));
Object.defineProperty(exports, "SetTraceNotification", ({ enumerable: true, get: function () { return connection_1.SetTraceNotification; } }));
Object.defineProperty(exports, "LogTraceNotification", ({ enumerable: true, get: function () { return connection_1.LogTraceNotification; } }));
Object.defineProperty(exports, "ConnectionErrors", ({ enumerable: true, get: function () { return connection_1.ConnectionErrors; } }));
Object.defineProperty(exports, "ConnectionError", ({ enumerable: true, get: function () { return connection_1.ConnectionError; } }));
Object.defineProperty(exports, "CancellationReceiverStrategy", ({ enumerable: true, get: function () { return connection_1.CancellationReceiverStrategy; } }));
Object.defineProperty(exports, "CancellationSenderStrategy", ({ enumerable: true, get: function () { return connection_1.CancellationSenderStrategy; } }));
Object.defineProperty(exports, "CancellationStrategy", ({ enumerable: true, get: function () { return connection_1.CancellationStrategy; } }));
Object.defineProperty(exports, "MessageStrategy", ({ enumerable: true, get: function () { return connection_1.MessageStrategy; } }));
const ral_1 = __webpack_require__(48094);
exports.RAL = ral_1.default;


/***/ }),

/***/ 97770:
/***/ ((__unused_webpack_module, exports, __webpack_require__) => {


/*---------------------------------------------------------------------------------------------
 *  Copyright (c) Microsoft Corporation. All rights reserved.
 *  Licensed under the MIT License. See License.txt in the project root for license information.
 *--------------------------------------------------------------------------------------------*/
Object.defineProperty(exports, "__esModule", ({ value: true }));
exports.CancellationTokenSource = exports.CancellationToken = void 0;
const ral_1 = __webpack_require__(48094);
const Is = __webpack_require__(78472);
const events_1 = __webpack_require__(345);
var CancellationToken;
(function (CancellationToken) {
    CancellationToken.None = Object.freeze({
        isCancellationRequested: false,
        onCancellationRequested: events_1.Event.None
    });
    CancellationToken.Cancelled = Object.freeze({
        isCancellationRequested: true,
        onCancellationRequested: events_1.Event.None
    });
    function is(value) {
        const candidate = value;
        return candidate && (candidate === CancellationToken.None
            || candidate === CancellationToken.Cancelled
            || (Is.boolean(candidate.isCancellationRequested) && !!candidate.onCancellationRequested));
    }
    CancellationToken.is = is;
})(CancellationToken || (exports.CancellationToken = CancellationToken = {}));
const shortcutEvent = Object.freeze(function (callback, context) {
    const handle = (0, ral_1.default)().timer.setTimeout(callback.bind(context), 0);
    return { dispose() { handle.dispose(); } };
});
class MutableToken {
    constructor() {
        this._isCancelled = false;
    }
    cancel() {
        if (!this._isCancelled) {
            this._isCancelled = true;
            if (this._emitter) {
                this._emitter.fire(undefined);
                this.dispose();
            }
        }
    }
    get isCancellationRequested() {
        return this._isCancelled;
    }
    get onCancellationRequested() {
        if (this._isCancelled) {
            return shortcutEvent;
        }
        if (!this._emitter) {
            this._emitter = new events_1.Emitter();
        }
        return this._emitter.event;
    }
    dispose() {
        if (this._emitter) {
            this._emitter.dispose();
            this._emitter = undefined;
        }
    }
}
class CancellationTokenSource {
    get token() {
        if (!this._token) {
            // be lazy and create the token only when
            // actually needed
            this._token = new MutableToken();
        }
        return this._token;
    }
    cancel() {
        if (!this._token) {
            // save an object by returning the default
            // cancelled token when cancellation happens
            // before someone asks for the token
            this._token = CancellationToken.Cancelled;
        }
        else {
            this._token.cancel();
        }
    }
    dispose() {
        if (!this._token) {
            // ensure to initialize with an empty token if we had none
            this._token = CancellationToken.None;
        }
        else if (this._token instanceof MutableToken) {
            // actually dispose
            this._token.dispose();
        }
    }
}
exports.CancellationTokenSource = CancellationTokenSource;


/***/ }),

/***/ 6336:
/***/ ((__unused_webpack_module, exports, __webpack_require__) => {


/* --------------------------------------------------------------------------------------------
 * Copyright (c) Microsoft Corporation. All rights reserved.
 * Licensed under the MIT License. See License.txt in the project root for license information.
 * ------------------------------------------------------------------------------------------ */
Object.defineProperty(exports, "__esModule", ({ value: true }));
exports.createMessageConnection = exports.ConnectionOptions = exports.MessageStrategy = exports.CancellationStrategy = exports.CancellationSenderStrategy = exports.CancellationReceiverStrategy = exports.RequestCancellationReceiverStrategy = exports.IdCancellationReceiverStrategy = exports.ConnectionStrategy = exports.ConnectionError = exports.ConnectionErrors = exports.LogTraceNotification = exports.SetTraceNotification = exports.TraceFormat = exports.TraceValues = exports.Trace = exports.NullLogger = exports.ProgressType = exports.ProgressToken = void 0;
const ral_1 = __webpack_require__(48094);
const Is = __webpack_require__(78472);
const messages_1 = __webpack_require__(75285);
const linkedMap_1 = __webpack_require__(45164);
const events_1 = __webpack_require__(345);
const cancellation_1 = __webpack_require__(97770);
var CancelNotification;
(function (CancelNotification) {
    CancelNotification.type = new messages_1.NotificationType('$/cancelRequest');
})(CancelNotification || (CancelNotification = {}));
var ProgressToken;
(function (ProgressToken) {
    function is(value) {
        return typeof value === 'string' || typeof value === 'number';
    }
    ProgressToken.is = is;
})(ProgressToken || (exports.ProgressToken = ProgressToken = {}));
var ProgressNotification;
(function (ProgressNotification) {
    ProgressNotification.type = new messages_1.NotificationType('$/progress');
})(ProgressNotification || (ProgressNotification = {}));
class ProgressType {
    constructor() {
    }
}
exports.ProgressType = ProgressType;
var StarRequestHandler;
(function (StarRequestHandler) {
    function is(value) {
        return Is.func(value);
    }
    StarRequestHandler.is = is;
})(StarRequestHandler || (StarRequestHandler = {}));
exports.NullLogger = Object.freeze({
    error: () => { },
    warn: () => { },
    info: () => { },
    log: () => { }
});
var Trace;
(function (Trace) {
    Trace[Trace["Off"] = 0] = "Off";
    Trace[Trace["Messages"] = 1] = "Messages";
    Trace[Trace["Compact"] = 2] = "Compact";
    Trace[Trace["Verbose"] = 3] = "Verbose";
})(Trace || (exports.Trace = Trace = {}));
var TraceValues;
(function (TraceValues) {
    /**
     * Turn tracing off.
     */
    TraceValues.Off = 'off';
    /**
     * Trace messages only.
     */
    TraceValues.Messages = 'messages';
    /**
     * Compact message tracing.
     */
    TraceValues.Compact = 'compact';
    /**
     * Verbose message tracing.
     */
    TraceValues.Verbose = 'verbose';
})(TraceValues || (exports.TraceValues = TraceValues = {}));
(function (Trace) {
    function fromString(value) {
        if (!Is.string(value)) {
            return Trace.Off;
        }
        value = value.toLowerCase();
        switch (value) {
            case 'off':
                return Trace.Off;
            case 'messages':
                return Trace.Messages;
            case 'compact':
                return Trace.Compact;
            case 'verbose':
                return Trace.Verbose;
            default:
                return Trace.Off;
        }
    }
    Trace.fromString = fromString;
    function toString(value) {
        switch (value) {
            case Trace.Off:
                return 'off';
            case Trace.Messages:
                return 'messages';
            case Trace.Compact:
                return 'compact';
            case Trace.Verbose:
                return 'verbose';
            default:
                return 'off';
        }
    }
    Trace.toString = toString;
})(Trace || (exports.Trace = Trace = {}));
var TraceFormat;
(function (TraceFormat) {
    TraceFormat["Text"] = "text";
    TraceFormat["JSON"] = "json";
})(TraceFormat || (exports.TraceFormat = TraceFormat = {}));
(function (TraceFormat) {
    function fromString(value) {
        if (!Is.string(value)) {
            return TraceFormat.Text;
        }
        value = value.toLowerCase();
        if (value === 'json') {
            return TraceFormat.JSON;
        }
        else {
            return TraceFormat.Text;
        }
    }
    TraceFormat.fromString = fromString;
})(TraceFormat || (exports.TraceFormat = TraceFormat = {}));
var SetTraceNotification;
(function (SetTraceNotification) {
    SetTraceNotification.type = new messages_1.NotificationType('$/setTrace');
})(SetTraceNotification || (exports.SetTraceNotification = SetTraceNotification = {}));
var LogTraceNotification;
(function (LogTraceNotification) {
    LogTraceNotification.type = new messages_1.NotificationType('$/logTrace');
})(LogTraceNotification || (exports.LogTraceNotification = LogTraceNotification = {}));
var ConnectionErrors;
(function (ConnectionErrors) {
    /**
     * The connection is closed.
     */
    ConnectionErrors[ConnectionErrors["Closed"] = 1] = "Closed";
    /**
     * The connection got disposed.
     */
    ConnectionErrors[ConnectionErrors["Disposed"] = 2] = "Disposed";
    /**
     * The connection is already in listening mode.
     */
    ConnectionErrors[ConnectionErrors["AlreadyListening"] = 3] = "AlreadyListening";
})(ConnectionErrors || (exports.ConnectionErrors = ConnectionErrors = {}));
class ConnectionError extends Error {
    constructor(code, message) {
        super(message);
        this.code = code;
        Object.setPrototypeOf(this, ConnectionError.prototype);
    }
}
exports.ConnectionError = ConnectionError;
var ConnectionStrategy;
(function (ConnectionStrategy) {
    function is(value) {
        const candidate = value;
        return candidate && Is.func(candidate.cancelUndispatched);
    }
    ConnectionStrategy.is = is;
})(ConnectionStrategy || (exports.ConnectionStrategy = ConnectionStrategy = {}));
var IdCancellationReceiverStrategy;
(function (IdCancellationReceiverStrategy) {
    function is(value) {
        const candidate = value;
        return candidate && (candidate.kind === undefined || candidate.kind === 'id') && Is.func(candidate.createCancellationTokenSource) && (candidate.dispose === undefined || Is.func(candidate.dispose));
    }
    IdCancellationReceiverStrategy.is = is;
})(IdCancellationReceiverStrategy || (exports.IdCancellationReceiverStrategy = IdCancellationReceiverStrategy = {}));
var RequestCancellationReceiverStrategy;
(function (RequestCancellationReceiverStrategy) {
    function is(value) {
        const candidate = value;
        return candidate && candidate.kind === 'request' && Is.func(candidate.createCancellationTokenSource) && (candidate.dispose === undefined || Is.func(candidate.dispose));
    }
    RequestCancellationReceiverStrategy.is = is;
})(RequestCancellationReceiverStrategy || (exports.RequestCancellationReceiverStrategy = RequestCancellationReceiverStrategy = {}));
var CancellationReceiverStrategy;
(function (CancellationReceiverStrategy) {
    CancellationReceiverStrategy.Message = Object.freeze({
        createCancellationTokenSource(_) {
            return new cancellation_1.CancellationTokenSource();
        }
    });
    function is(value) {
        return IdCancellationReceiverStrategy.is(value) || RequestCancellationReceiverStrategy.is(value);
    }
    CancellationReceiverStrategy.is = is;
})(CancellationReceiverStrategy || (exports.CancellationReceiverStrategy = CancellationReceiverStrategy = {}));
var CancellationSenderStrategy;
(function (CancellationSenderStrategy) {
    CancellationSenderStrategy.Message = Object.freeze({
        sendCancellation(conn, id) {
            return conn.sendNotification(CancelNotification.type, { id });
        },
        cleanup(_) { }
    });
    function is(value) {
        const candidate = value;
        return candidate && Is.func(candidate.sendCancellation) && Is.func(candidate.cleanup);
    }
    CancellationSenderStrategy.is = is;
})(CancellationSenderStrategy || (exports.CancellationSenderStrategy = CancellationSenderStrategy = {}));
var CancellationStrategy;
(function (CancellationStrategy) {
    CancellationStrategy.Message = Object.freeze({
        receiver: CancellationReceiverStrategy.Message,
        sender: CancellationSenderStrategy.Message
    });
    function is(value) {
        const candidate = value;
        return candidate && CancellationReceiverStrategy.is(candidate.receiver) && CancellationSenderStrategy.is(candidate.sender);
    }
    CancellationStrategy.is = is;
})(CancellationStrategy || (exports.CancellationStrategy = CancellationStrategy = {}));
var MessageStrategy;
(function (MessageStrategy) {
    function is(value) {
        const candidate = value;
        return candidate && Is.func(candidate.handleMessage);
    }
    MessageStrategy.is = is;
})(MessageStrategy || (exports.MessageStrategy = MessageStrategy = {}));
var ConnectionOptions;
(function (ConnectionOptions) {
    function is(value) {
        const candidate = value;
        return candidate && (CancellationStrategy.is(candidate.cancellationStrategy) || ConnectionStrategy.is(candidate.connectionStrategy) || MessageStrategy.is(candidate.messageStrategy));
    }
    ConnectionOptions.is = is;
})(ConnectionOptions || (exports.ConnectionOptions = ConnectionOptions = {}));
var ConnectionState;
(function (ConnectionState) {
    ConnectionState[ConnectionState["New"] = 1] = "New";
    ConnectionState[ConnectionState["Listening"] = 2] = "Listening";
    ConnectionState[ConnectionState["Closed"] = 3] = "Closed";
    ConnectionState[ConnectionState["Disposed"] = 4] = "Disposed";
})(ConnectionState || (ConnectionState = {}));
function createMessageConnection(messageReader, messageWriter, _logger, options) {
    const logger = _logger !== undefined ? _logger : exports.NullLogger;
    let sequenceNumber = 0;
    let notificationSequenceNumber = 0;
    let unknownResponseSequenceNumber = 0;
    const version = '2.0';
    let starRequestHandler = undefined;
    const requestHandlers = new Map();
    let starNotificationHandler = undefined;
    const notificationHandlers = new Map();
    const progressHandlers = new Map();
    let timer;
    let messageQueue = new linkedMap_1.LinkedMap();
    let responsePromises = new Map();
    let knownCanceledRequests = new Set();
    let requestTokens = new Map();
    let trace = Trace.Off;
    let traceFormat = TraceFormat.Text;
    let tracer;
    let state = ConnectionState.New;
    const errorEmitter = new events_1.Emitter();
    const closeEmitter = new events_1.Emitter();
    const unhandledNotificationEmitter = new events_1.Emitter();
    const unhandledProgressEmitter = new events_1.Emitter();
    const disposeEmitter = new events_1.Emitter();
    const cancellationStrategy = (options && options.cancellationStrategy) ? options.cancellationStrategy : CancellationStrategy.Message;
    function createRequestQueueKey(id) {
        if (id === null) {
            throw new Error(`Can't send requests with id null since the response can't be correlated.`);
        }
        return 'req-' + id.toString();
    }
    function createResponseQueueKey(id) {
        if (id === null) {
            return 'res-unknown-' + (++unknownResponseSequenceNumber).toString();
        }
        else {
            return 'res-' + id.toString();
        }
    }
    function createNotificationQueueKey() {
        return 'not-' + (++notificationSequenceNumber).toString();
    }
    function addMessageToQueue(queue, message) {
        if (messages_1.Message.isRequest(message)) {
            queue.set(createRequestQueueKey(message.id), message);
        }
        else if (messages_1.Message.isResponse(message)) {
            queue.set(createResponseQueueKey(message.id), message);
        }
        else {
            queue.set(createNotificationQueueKey(), message);
        }
    }
    function cancelUndispatched(_message) {
        return undefined;
    }
    function isListening() {
        return state === ConnectionState.Listening;
    }
    function isClosed() {
        return state === ConnectionState.Closed;
    }
    function isDisposed() {
        return state === ConnectionState.Disposed;
    }
    function closeHandler() {
        if (state === ConnectionState.New || state === ConnectionState.Listening) {
            state = ConnectionState.Closed;
            closeEmitter.fire(undefined);
        }
        // If the connection is disposed don't sent close events.
    }
    function readErrorHandler(error) {
        errorEmitter.fire([error, undefined, undefined]);
    }
    function writeErrorHandler(data) {
        errorEmitter.fire(data);
    }
    messageReader.onClose(closeHandler);
    messageReader.onError(readErrorHandler);
    messageWriter.onClose(closeHandler);
    messageWriter.onError(writeErrorHandler);
    function triggerMessageQueue() {
        if (timer || messageQueue.size === 0) {
            return;
        }
        timer = (0, ral_1.default)().timer.setImmediate(() => {
            timer = undefined;
            processMessageQueue();
        });
    }
    function handleMessage(message) {
        if (messages_1.Message.isRequest(message)) {
            handleRequest(message);
        }
        else if (messages_1.Message.isNotification(message)) {
            handleNotification(message);
        }
        else if (messages_1.Message.isResponse(message)) {
            handleResponse(message);
        }
        else {
            handleInvalidMessage(message);
        }
    }
    function processMessageQueue() {
        if (messageQueue.size === 0) {
            return;
        }
        const message = messageQueue.shift();
        try {
            const messageStrategy = options?.messageStrategy;
            if (MessageStrategy.is(messageStrategy)) {
                messageStrategy.handleMessage(message, handleMessage);
            }
            else {
                handleMessage(message);
            }
        }
        finally {
            triggerMessageQueue();
        }
    }
    const callback = (message) => {
        try {
            // We have received a cancellation message. Check if the message is still in the queue
            // and cancel it if allowed to do so.
            if (messages_1.Message.isNotification(message) && message.method === CancelNotification.type.method) {
                const cancelId = message.params.id;
                const key = createRequestQueueKey(cancelId);
                const toCancel = messageQueue.get(key);
                if (messages_1.Message.isRequest(toCancel)) {
                    const strategy = options?.connectionStrategy;
                    const response = (strategy && strategy.cancelUndispatched) ? strategy.cancelUndispatched(toCancel, cancelUndispatched) : cancelUndispatched(toCancel);
                    if (response && (response.error !== undefined || response.result !== undefined)) {
                        messageQueue.delete(key);
                        requestTokens.delete(cancelId);
                        response.id = toCancel.id;
                        traceSendingResponse(response, message.method, Date.now());
                        messageWriter.write(response).catch(() => logger.error(`Sending response for canceled message failed.`));
                        return;
                    }
                }
                const cancellationToken = requestTokens.get(cancelId);
                // The request is already running. Cancel the token
                if (cancellationToken !== undefined) {
                    cancellationToken.cancel();
                    traceReceivedNotification(message);
                    return;
                }
                else {
                    // Remember the cancel but still queue the message to
                    // clean up state in process message.
                    knownCanceledRequests.add(cancelId);
                }
            }
            addMessageToQueue(messageQueue, message);
        }
        finally {
            triggerMessageQueue();
        }
    };
    function handleRequest(requestMessage) {
        if (isDisposed()) {
            // we return here silently since we fired an event when the
            // connection got disposed.
            return;
        }
        function reply(resultOrError, method, startTime) {
            const message = {
                jsonrpc: version,
                id: requestMessage.id
            };
            if (resultOrError instanceof messages_1.ResponseError) {
                message.error = resultOrError.toJson();
            }
            else {
                message.result = resultOrError === undefined ? null : resultOrError;
            }
            traceSendingResponse(message, method, startTime);
            messageWriter.write(message).catch(() => logger.error(`Sending response failed.`));
        }
        function replyError(error, method, startTime) {
            const message = {
                jsonrpc: version,
                id: requestMessage.id,
                error: error.toJson()
            };
            traceSendingResponse(message, method, startTime);
            messageWriter.write(message).catch(() => logger.error(`Sending response failed.`));
        }
        function replySuccess(result, method, startTime) {
            // The JSON RPC defines that a response must either have a result or an error
            // So we can't treat undefined as a valid response result.
            if (result === undefined) {
                result = null;
            }
            const message = {
                jsonrpc: version,
                id: requestMessage.id,
                result: result
            };
            traceSendingResponse(message, method, startTime);
            messageWriter.write(message).catch(() => logger.error(`Sending response failed.`));
        }
        traceReceivedRequest(requestMessage);
        const element = requestHandlers.get(requestMessage.method);
        let type;
        let requestHandler;
        if (element) {
            type = element.type;
            requestHandler = element.handler;
        }
        const startTime = Date.now();
        if (requestHandler || starRequestHandler) {
            const tokenKey = requestMessage.id ?? String(Date.now()); //
            const cancellationSource = IdCancellationReceiverStrategy.is(cancellationStrategy.receiver)
                ? cancellationStrategy.receiver.createCancellationTokenSource(tokenKey)
                : cancellationStrategy.receiver.createCancellationTokenSource(requestMessage);
            if (requestMessage.id !== null && knownCanceledRequests.has(requestMessage.id)) {
                cancellationSource.cancel();
            }
            if (requestMessage.id !== null) {
                requestTokens.set(tokenKey, cancellationSource);
            }
            try {
                let handlerResult;
                if (requestHandler) {
                    if (requestMessage.params === undefined) {
                        if (type !== undefined && type.numberOfParams !== 0) {
                            replyError(new messages_1.ResponseError(messages_1.ErrorCodes.InvalidParams, `Request ${requestMessage.method} defines ${type.numberOfParams} params but received none.`), requestMessage.method, startTime);
                            return;
                        }
                        handlerResult = requestHandler(cancellationSource.token);
                    }
                    else if (Array.isArray(requestMessage.params)) {
                        if (type !== undefined && type.parameterStructures === messages_1.ParameterStructures.byName) {
                            replyError(new messages_1.ResponseError(messages_1.ErrorCodes.InvalidParams, `Request ${requestMessage.method} defines parameters by name but received parameters by position`), requestMessage.method, startTime);
                            return;
                        }
                        handlerResult = requestHandler(...requestMessage.params, cancellationSource.token);
                    }
                    else {
                        if (type !== undefined && type.parameterStructures === messages_1.ParameterStructures.byPosition) {
                            replyError(new messages_1.ResponseError(messages_1.ErrorCodes.InvalidParams, `Request ${requestMessage.method} defines parameters by position but received parameters by name`), requestMessage.method, startTime);
                            return;
                        }
                        handlerResult = requestHandler(requestMessage.params, cancellationSource.token);
                    }
                }
                else if (starRequestHandler) {
                    handlerResult = starRequestHandler(requestMessage.method, requestMessage.params, cancellationSource.token);
                }
                const promise = handlerResult;
                if (!handlerResult) {
                    requestTokens.delete(tokenKey);
                    replySuccess(handlerResult, requestMessage.method, startTime);
                }
                else if (promise.then) {
                    promise.then((resultOrError) => {
                        requestTokens.delete(tokenKey);
                        reply(resultOrError, requestMessage.method, startTime);
                    }, error => {
                        requestTokens.delete(tokenKey);
                        if (error instanceof messages_1.ResponseError) {
                            replyError(error, requestMessage.method, startTime);
                        }
                        else if (error && Is.string(error.message)) {
                            replyError(new messages_1.ResponseError(messages_1.ErrorCodes.InternalError, `Request ${requestMessage.method} failed with message: ${error.message}`), requestMessage.method, startTime);
                        }
                        else {
                            replyError(new messages_1.ResponseError(messages_1.ErrorCodes.InternalError, `Request ${requestMessage.method} failed unexpectedly without providing any details.`), requestMessage.method, startTime);
                        }
                    });
                }
                else {
                    requestTokens.delete(tokenKey);
                    reply(handlerResult, requestMessage.method, startTime);
                }
            }
            catch (error) {
                requestTokens.delete(tokenKey);
                if (error instanceof messages_1.ResponseError) {
                    reply(error, requestMessage.method, startTime);
                }
                else if (error && Is.string(error.message)) {
                    replyError(new messages_1.ResponseError(messages_1.ErrorCodes.InternalError, `Request ${requestMessage.method} failed with message: ${error.message}`), requestMessage.method, startTime);
                }
                else {
                    replyError(new messages_1.ResponseError(messages_1.ErrorCodes.InternalError, `Request ${requestMessage.method} failed unexpectedly without providing any details.`), requestMessage.method, startTime);
                }
            }
        }
        else {
            replyError(new messages_1.ResponseError(messages_1.ErrorCodes.MethodNotFound, `Unhandled method ${requestMessage.method}`), requestMessage.method, startTime);
        }
    }
    function handleResponse(responseMessage) {
        if (isDisposed()) {
            // See handle request.
            return;
        }
        if (responseMessage.id === null) {
            if (responseMessage.error) {
                logger.error(`Received response message without id: Error is: \n${JSON.stringify(responseMessage.error, undefined, 4)}`);
            }
            else {
                logger.error(`Received response message without id. No further error information provided.`);
            }
        }
        else {
            const key = responseMessage.id;
            const responsePromise = responsePromises.get(key);
            traceReceivedResponse(responseMessage, responsePromise);
            if (responsePromise !== undefined) {
                responsePromises.delete(key);
                try {
                    if (responseMessage.error) {
                        const error = responseMessage.error;
                        responsePromise.reject(new messages_1.ResponseError(error.code, error.message, error.data));
                    }
                    else if (responseMessage.result !== undefined) {
                        responsePromise.resolve(responseMessage.result);
                    }
                    else {
                        throw new Error('Should never happen.');
                    }
                }
                catch (error) {
                    if (error.message) {
                        logger.error(`Response handler '${responsePromise.method}' failed with message: ${error.message}`);
                    }
                    else {
                        logger.error(`Response handler '${responsePromise.method}' failed unexpectedly.`);
                    }
                }
            }
        }
    }
    function handleNotification(message) {
        if (isDisposed()) {
            // See handle request.
            return;
        }
        let type = undefined;
        let notificationHandler;
        if (message.method === CancelNotification.type.method) {
            const cancelId = message.params.id;
            knownCanceledRequests.delete(cancelId);
            traceReceivedNotification(message);
            return;
        }
        else {
            const element = notificationHandlers.get(message.method);
            if (element) {
                notificationHandler = element.handler;
                type = element.type;
            }
        }
        if (notificationHandler || starNotificationHandler) {
            try {
                traceReceivedNotification(message);
                if (notificationHandler) {
                    if (message.params === undefined) {
                        if (type !== undefined) {
                            if (type.numberOfParams !== 0 && type.parameterStructures !== messages_1.ParameterStructures.byName) {
                                logger.error(`Notification ${message.method} defines ${type.numberOfParams} params but received none.`);
                            }
                        }
                        notificationHandler();
                    }
                    else if (Array.isArray(message.params)) {
                        // There are JSON-RPC libraries that send progress message as positional params although
                        // specified as named. So convert them if this is the case.
                        const params = message.params;
                        if (message.method === ProgressNotification.type.method && params.length === 2 && ProgressToken.is(params[0])) {
                            notificationHandler({ token: params[0], value: params[1] });
                        }
                        else {
                            if (type !== undefined) {
                                if (type.parameterStructures === messages_1.ParameterStructures.byName) {
                                    logger.error(`Notification ${message.method} defines parameters by name but received parameters by position`);
                                }
                                if (type.numberOfParams !== message.params.length) {
                                    logger.error(`Notification ${message.method} defines ${type.numberOfParams} params but received ${params.length} arguments`);
                                }
                            }
                            notificationHandler(...params);
                        }
                    }
                    else {
                        if (type !== undefined && type.parameterStructures === messages_1.ParameterStructures.byPosition) {
                            logger.error(`Notification ${message.method} defines parameters by position but received parameters by name`);
                        }
                        notificationHandler(message.params);
                    }
                }
                else if (starNotificationHandler) {
                    starNotificationHandler(message.method, message.params);
                }
            }
            catch (error) {
                if (error.message) {
                    logger.error(`Notification handler '${message.method}' failed with message: ${error.message}`);
                }
                else {
                    logger.error(`Notification handler '${message.method}' failed unexpectedly.`);
                }
            }
        }
        else {
            unhandledNotificationEmitter.fire(message);
        }
    }
    function handleInvalidMessage(message) {
        if (!message) {
            logger.error('Received empty message.');
            return;
        }
        logger.error(`Received message which is neither a response nor a notification message:\n${JSON.stringify(message, null, 4)}`);
        // Test whether we find an id to reject the promise
        const responseMessage = message;
        if (Is.string(responseMessage.id) || Is.number(responseMessage.id)) {
            const key = responseMessage.id;
            const responseHandler = responsePromises.get(key);
            if (responseHandler) {
                responseHandler.reject(new Error('The received response has neither a result nor an error property.'));
            }
        }
    }
    function stringifyTrace(params) {
        if (params === undefined || params === null) {
            return undefined;
        }
        switch (trace) {
            case Trace.Verbose:
                return JSON.stringify(params, null, 4);
            case Trace.Compact:
                return JSON.stringify(params);
            default:
                return undefined;
        }
    }
    function traceSendingRequest(message) {
        if (trace === Trace.Off || !tracer) {
            return;
        }
        if (traceFormat === TraceFormat.Text) {
            let data = undefined;
            if ((trace === Trace.Verbose || trace === Trace.Compact) && message.params) {
                data = `Params: ${stringifyTrace(message.params)}\n\n`;
            }
            tracer.log(`Sending request '${message.method} - (${message.id})'.`, data);
        }
        else {
            logLSPMessage('send-request', message);
        }
    }
    function traceSendingNotification(message) {
        if (trace === Trace.Off || !tracer) {
            return;
        }
        if (traceFormat === TraceFormat.Text) {
            let data = undefined;
            if (trace === Trace.Verbose || trace === Trace.Compact) {
                if (message.params) {
                    data = `Params: ${stringifyTrace(message.params)}\n\n`;
                }
                else {
                    data = 'No parameters provided.\n\n';
                }
            }
            tracer.log(`Sending notification '${message.method}'.`, data);
        }
        else {
            logLSPMessage('send-notification', message);
        }
    }
    function traceSendingResponse(message, method, startTime) {
        if (trace === Trace.Off || !tracer) {
            return;
        }
        if (traceFormat === TraceFormat.Text) {
            let data = undefined;
            if (trace === Trace.Verbose || trace === Trace.Compact) {
                if (message.error && message.error.data) {
                    data = `Error data: ${stringifyTrace(message.error.data)}\n\n`;
                }
                else {
                    if (message.result) {
                        data = `Result: ${stringifyTrace(message.result)}\n\n`;
                    }
                    else if (message.error === undefined) {
                        data = 'No result returned.\n\n';
                    }
                }
            }
            tracer.log(`Sending response '${method} - (${message.id})'. Processing request took ${Date.now() - startTime}ms`, data);
        }
        else {
            logLSPMessage('send-response', message);
        }
    }
    function traceReceivedRequest(message) {
        if (trace === Trace.Off || !tracer) {
            return;
        }
        if (traceFormat === TraceFormat.Text) {
            let data = undefined;
            if ((trace === Trace.Verbose || trace === Trace.Compact) && message.params) {
                data = `Params: ${stringifyTrace(message.params)}\n\n`;
            }
            tracer.log(`Received request '${message.method} - (${message.id})'.`, data);
        }
        else {
            logLSPMessage('receive-request', message);
        }
    }
    function traceReceivedNotification(message) {
        if (trace === Trace.Off || !tracer || message.method === LogTraceNotification.type.method) {
            return;
        }
        if (traceFormat === TraceFormat.Text) {
            let data = undefined;
            if (trace === Trace.Verbose || trace === Trace.Compact) {
                if (message.params) {
                    data = `Params: ${stringifyTrace(message.params)}\n\n`;
                }
                else {
                    data = 'No parameters provided.\n\n';
                }
            }
            tracer.log(`Received notification '${message.method}'.`, data);
        }
        else {
            logLSPMessage('receive-notification', message);
        }
    }
    function traceReceivedResponse(message, responsePromise) {
        if (trace === Trace.Off || !tracer) {
            return;
        }
        if (traceFormat === TraceFormat.Text) {
            let data = undefined;
            if (trace === Trace.Verbose || trace === Trace.Compact) {
                if (message.error && message.error.data) {
                    data = `Error data: ${stringifyTrace(message.error.data)}\n\n`;
                }
                else {
                    if (message.result) {
                        data = `Result: ${stringifyTrace(message.result)}\n\n`;
                    }
                    else if (message.error === undefined) {
                        data = 'No result returned.\n\n';
                    }
                }
            }
            if (responsePromise) {
                const error = message.error ? ` Request failed: ${message.error.message} (${message.error.code}).` : '';
                tracer.log(`Received response '${responsePromise.method} - (${message.id})' in ${Date.now() - responsePromise.timerStart}ms.${error}`, data);
            }
            else {
                tracer.log(`Received response ${message.id} without active response promise.`, data);
            }
        }
        else {
            logLSPMessage('receive-response', message);
        }
    }
    function logLSPMessage(type, message) {
        if (!tracer || trace === Trace.Off) {
            return;
        }
        const lspMessage = {
            isLSPMessage: true,
            type,
            message,
            timestamp: Date.now()
        };
        tracer.log(lspMessage);
    }
    function throwIfClosedOrDisposed() {
        if (isClosed()) {
            throw new ConnectionError(ConnectionErrors.Closed, 'Connection is closed.');
        }
        if (isDisposed()) {
            throw new ConnectionError(ConnectionErrors.Disposed, 'Connection is disposed.');
        }
    }
    function throwIfListening() {
        if (isListening()) {
            throw new ConnectionError(ConnectionErrors.AlreadyListening, 'Connection is already listening');
        }
    }
    function throwIfNotListening() {
        if (!isListening()) {
            throw new Error('Call listen() first.');
        }
    }
    function undefinedToNull(param) {
        if (param === undefined) {
            return null;
        }
        else {
            return param;
        }
    }
    function nullToUndefined(param) {
        if (param === null) {
            return undefined;
        }
        else {
            return param;
        }
    }
    function isNamedParam(param) {
        return param !== undefined && param !== null && !Array.isArray(param) && typeof param === 'object';
    }
    function computeSingleParam(parameterStructures, param) {
        switch (parameterStructures) {
            case messages_1.ParameterStructures.auto:
                if (isNamedParam(param)) {
                    return nullToUndefined(param);
                }
                else {
                    return [undefinedToNull(param)];
                }
            case messages_1.ParameterStructures.byName:
                if (!isNamedParam(param)) {
                    throw new Error(`Received parameters by name but param is not an object literal.`);
                }
                return nullToUndefined(param);
            case messages_1.ParameterStructures.byPosition:
                return [undefinedToNull(param)];
            default:
                throw new Error(`Unknown parameter structure ${parameterStructures.toString()}`);
        }
    }
    function computeMessageParams(type, params) {
        let result;
        const numberOfParams = type.numberOfParams;
        switch (numberOfParams) {
            case 0:
                result = undefined;
                break;
            case 1:
                result = computeSingleParam(type.parameterStructures, params[0]);
                break;
            default:
                result = [];
                for (let i = 0; i < params.length && i < numberOfParams; i++) {
                    result.push(undefinedToNull(params[i]));
                }
                if (params.length < numberOfParams) {
                    for (let i = params.length; i < numberOfParams; i++) {
                        result.push(null);
                    }
                }
                break;
        }
        return result;
    }
    const connection = {
        sendNotification: (type, ...args) => {
            throwIfClosedOrDisposed();
            let method;
            let messageParams;
            if (Is.string(type)) {
                method = type;
                const first = args[0];
                let paramStart = 0;
                let parameterStructures = messages_1.ParameterStructures.auto;
                if (messages_1.ParameterStructures.is(first)) {
                    paramStart = 1;
                    parameterStructures = first;
                }
                let paramEnd = args.length;
                const numberOfParams = paramEnd - paramStart;
                switch (numberOfParams) {
                    case 0:
                        messageParams = undefined;
                        break;
                    case 1:
                        messageParams = computeSingleParam(parameterStructures, args[paramStart]);
                        break;
                    default:
                        if (parameterStructures === messages_1.ParameterStructures.byName) {
                            throw new Error(`Received ${numberOfParams} parameters for 'by Name' notification parameter structure.`);
                        }
                        messageParams = args.slice(paramStart, paramEnd).map(value => undefinedToNull(value));
                        break;
                }
            }
            else {
                const params = args;
                method = type.method;
                messageParams = computeMessageParams(type, params);
            }
            const notificationMessage = {
                jsonrpc: version,
                method: method,
                params: messageParams
            };
            traceSendingNotification(notificationMessage);
            return messageWriter.write(notificationMessage).catch((error) => {
                logger.error(`Sending notification failed.`);
                throw error;
            });
        },
        onNotification: (type, handler) => {
            throwIfClosedOrDisposed();
            let method;
            if (Is.func(type)) {
                starNotificationHandler = type;
            }
            else if (handler) {
                if (Is.string(type)) {
                    method = type;
                    notificationHandlers.set(type, { type: undefined, handler });
                }
                else {
                    method = type.method;
                    notificationHandlers.set(type.method, { type, handler });
                }
            }
            return {
                dispose: () => {
                    if (method !== undefined) {
                        notificationHandlers.delete(method);
                    }
                    else {
                        starNotificationHandler = undefined;
                    }
                }
            };
        },
        onProgress: (_type, token, handler) => {
            if (progressHandlers.has(token)) {
                throw new Error(`Progress handler for token ${token} already registered`);
            }
            progressHandlers.set(token, handler);
            return {
                dispose: () => {
                    progressHandlers.delete(token);
                }
            };
        },
        sendProgress: (_type, token, value) => {
            // This should not await but simple return to ensure that we don't have another
            // async scheduling. Otherwise one send could overtake another send.
            return connection.sendNotification(ProgressNotification.type, { token, value });
        },
        onUnhandledProgress: unhandledProgressEmitter.event,
        sendRequest: (type, ...args) => {
            throwIfClosedOrDisposed();
            throwIfNotListening();
            let method;
            let messageParams;
            let token = undefined;
            if (Is.string(type)) {
                method = type;
                const first = args[0];
                const last = args[args.length - 1];
                let paramStart = 0;
                let parameterStructures = messages_1.ParameterStructures.auto;
                if (messages_1.ParameterStructures.is(first)) {
                    paramStart = 1;
                    parameterStructures = first;
                }
                let paramEnd = args.length;
                if (cancellation_1.CancellationToken.is(last)) {
                    paramEnd = paramEnd - 1;
                    token = last;
                }
                const numberOfParams = paramEnd - paramStart;
                switch (numberOfParams) {
                    case 0:
                        messageParams = undefined;
                        break;
                    case 1:
                        messageParams = computeSingleParam(parameterStructures, args[paramStart]);
                        break;
                    default:
                        if (parameterStructures === messages_1.ParameterStructures.byName) {
                            throw new Error(`Received ${numberOfParams} parameters for 'by Name' request parameter structure.`);
                        }
                        messageParams = args.slice(paramStart, paramEnd).map(value => undefinedToNull(value));
                        break;
                }
            }
            else {
                const params = args;
                method = type.method;
                messageParams = computeMessageParams(type, params);
                const numberOfParams = type.numberOfParams;
                token = cancellation_1.CancellationToken.is(params[numberOfParams]) ? params[numberOfParams] : undefined;
            }
            const id = sequenceNumber++;
            let disposable;
            if (token) {
                disposable = token.onCancellationRequested(() => {
                    const p = cancellationStrategy.sender.sendCancellation(connection, id);
                    if (p === undefined) {
                        logger.log(`Received no promise from cancellation strategy when cancelling id ${id}`);
                        return Promise.resolve();
                    }
                    else {
                        return p.catch(() => {
                            logger.log(`Sending cancellation messages for id ${id} failed`);
                        });
                    }
                });
            }
            const requestMessage = {
                jsonrpc: version,
                id: id,
                method: method,
                params: messageParams
            };
            traceSendingRequest(requestMessage);
            if (typeof cancellationStrategy.sender.enableCancellation === 'function') {
                cancellationStrategy.sender.enableCancellation(requestMessage);
            }
            return new Promise(async (resolve, reject) => {
                const resolveWithCleanup = (r) => {
                    resolve(r);
                    cancellationStrategy.sender.cleanup(id);
                    disposable?.dispose();
                };
                const rejectWithCleanup = (r) => {
                    reject(r);
                    cancellationStrategy.sender.cleanup(id);
                    disposable?.dispose();
                };
                const responsePromise = { method: method, timerStart: Date.now(), resolve: resolveWithCleanup, reject: rejectWithCleanup };
                try {
                    await messageWriter.write(requestMessage);
                    responsePromises.set(id, responsePromise);
                }
                catch (error) {
                    logger.error(`Sending request failed.`);
                    // Writing the message failed. So we need to reject the promise.
                    responsePromise.reject(new messages_1.ResponseError(messages_1.ErrorCodes.MessageWriteError, error.message ? error.message : 'Unknown reason'));
                    throw error;
                }
            });
        },
        onRequest: (type, handler) => {
            throwIfClosedOrDisposed();
            let method = null;
            if (StarRequestHandler.is(type)) {
                method = undefined;
                starRequestHandler = type;
            }
            else if (Is.string(type)) {
                method = null;
                if (handler !== undefined) {
                    method = type;
                    requestHandlers.set(type, { handler: handler, type: undefined });
                }
            }
            else {
                if (handler !== undefined) {
                    method = type.method;
                    requestHandlers.set(type.method, { type, handler });
                }
            }
            return {
                dispose: () => {
                    if (method === null) {
                        return;
                    }
                    if (method !== undefined) {
                        requestHandlers.delete(method);
                    }
                    else {
                        starRequestHandler = undefined;
                    }
                }
            };
        },
        hasPendingResponse: () => {
            return responsePromises.size > 0;
        },
        trace: async (_value, _tracer, sendNotificationOrTraceOptions) => {
            let _sendNotification = false;
            let _traceFormat = TraceFormat.Text;
            if (sendNotificationOrTraceOptions !== undefined) {
                if (Is.boolean(sendNotificationOrTraceOptions)) {
                    _sendNotification = sendNotificationOrTraceOptions;
                }
                else {
                    _sendNotification = sendNotificationOrTraceOptions.sendNotification || false;
                    _traceFormat = sendNotificationOrTraceOptions.traceFormat || TraceFormat.Text;
                }
            }
            trace = _value;
            traceFormat = _traceFormat;
            if (trace === Trace.Off) {
                tracer = undefined;
            }
            else {
                tracer = _tracer;
            }
            if (_sendNotification && !isClosed() && !isDisposed()) {
                await connection.sendNotification(SetTraceNotification.type, { value: Trace.toString(_value) });
            }
        },
        onError: errorEmitter.event,
        onClose: closeEmitter.event,
        onUnhandledNotification: unhandledNotificationEmitter.event,
        onDispose: disposeEmitter.event,
        end: () => {
            messageWriter.end();
        },
        dispose: () => {
            if (isDisposed()) {
                return;
            }
            state = ConnectionState.Disposed;
            disposeEmitter.fire(undefined);
            const error = new messages_1.ResponseError(messages_1.ErrorCodes.PendingResponseRejected, 'Pending response rejected since connection got disposed');
            for (const promise of responsePromises.values()) {
                promise.reject(error);
            }
            responsePromises = new Map();
            requestTokens = new Map();
            knownCanceledRequests = new Set();
            messageQueue = new linkedMap_1.LinkedMap();
            // Test for backwards compatibility
            if (Is.func(messageWriter.dispose)) {
                messageWriter.dispose();
            }
            if (Is.func(messageReader.dispose)) {
                messageReader.dispose();
            }
        },
        listen: () => {
            throwIfClosedOrDisposed();
            throwIfListening();
            state = ConnectionState.Listening;
            messageReader.listen(callback);
        },
        inspect: () => {
            // eslint-disable-next-line no-console
            (0, ral_1.default)().console.log('inspect');
        }
    };
    connection.onNotification(LogTraceNotification.type, (params) => {
        if (trace === Trace.Off || !tracer) {
            return;
        }
        const verbose = trace === Trace.Verbose || trace === Trace.Compact;
        tracer.log(params.message, verbose ? params.verbose : undefined);
    });
    connection.onNotification(ProgressNotification.type, (params) => {
        const handler = progressHandlers.get(params.token);
        if (handler) {
            handler(params.value);
        }
        else {
            unhandledProgressEmitter.fire(params);
        }
    });
    return connection;
}
exports.createMessageConnection = createMessageConnection;


/***/ }),

/***/ 68159:
/***/ ((__unused_webpack_module, exports) => {


/*---------------------------------------------------------------------------------------------
 *  Copyright (c) Microsoft Corporation. All rights reserved.
 *  Licensed under the MIT License. See License.txt in the project root for license information.
 *--------------------------------------------------------------------------------------------*/
Object.defineProperty(exports, "__esModule", ({ value: true }));
exports.Disposable = void 0;
var Disposable;
(function (Disposable) {
    function create(func) {
        return {
            dispose: func
        };
    }
    Disposable.create = create;
})(Disposable || (exports.Disposable = Disposable = {}));


/***/ }),

/***/ 345:
/***/ ((__unused_webpack_module, exports, __webpack_require__) => {


/* --------------------------------------------------------------------------------------------
 * Copyright (c) Microsoft Corporation. All rights reserved.
 * Licensed under the MIT License. See License.txt in the project root for license information.
 * ------------------------------------------------------------------------------------------ */
Object.defineProperty(exports, "__esModule", ({ value: true }));
exports.Emitter = exports.Event = void 0;
const ral_1 = __webpack_require__(48094);
var Event;
(function (Event) {
    const _disposable = { dispose() { } };
    Event.None = function () { return _disposable; };
})(Event || (exports.Event = Event = {}));
class CallbackList {
    add(callback, context = null, bucket) {
        if (!this._callbacks) {
            this._callbacks = [];
            this._contexts = [];
        }
        this._callbacks.push(callback);
        this._contexts.push(context);
        if (Array.isArray(bucket)) {
            bucket.push({ dispose: () => this.remove(callback, context) });
        }
    }
    remove(callback, context = null) {
        if (!this._callbacks) {
            return;
        }
        let foundCallbackWithDifferentContext = false;
        for (let i = 0, len = this._callbacks.length; i < len; i++) {
            if (this._callbacks[i] === callback) {
                if (this._contexts[i] === context) {
                    // callback & context match => remove it
                    this._callbacks.splice(i, 1);
                    this._contexts.splice(i, 1);
                    return;
                }
                else {
                    foundCallbackWithDifferentContext = true;
                }
            }
        }
        if (foundCallbackWithDifferentContext) {
            throw new Error('When adding a listener with a context, you should remove it with the same context');
        }
    }
    invoke(...args) {
        if (!this._callbacks) {
            return [];
        }
        const ret = [], callbacks = this._callbacks.slice(0), contexts = this._contexts.slice(0);
        for (let i = 0, len = callbacks.length; i < len; i++) {
            try {
                ret.push(callbacks[i].apply(contexts[i], args));
            }
            catch (e) {
                // eslint-disable-next-line no-console
                (0, ral_1.default)().console.error(e);
            }
        }
        return ret;
    }
    isEmpty() {
        return !this._callbacks || this._callbacks.length === 0;
    }
    dispose() {
        this._callbacks = undefined;
        this._contexts = undefined;
    }
}
class Emitter {
    constructor(_options) {
        this._options = _options;
    }
    /**
     * For the public to allow to subscribe
     * to events from this Emitter
     */
    get event() {
        if (!this._event) {
            this._event = (listener, thisArgs, disposables) => {
                if (!this._callbacks) {
                    this._callbacks = new CallbackList();
                }
                if (this._options && this._options.onFirstListenerAdd && this._callbacks.isEmpty()) {
                    this._options.onFirstListenerAdd(this);
                }
                this._callbacks.add(listener, thisArgs);
                const result = {
                    dispose: () => {
                        if (!this._callbacks) {
                            // disposable is disposed after emitter is disposed.
                            return;
                        }
                        this._callbacks.remove(listener, thisArgs);
                        result.dispose = Emitter._noop;
                        if (this._options && this._options.onLastListenerRemove && this._callbacks.isEmpty()) {
                            this._options.onLastListenerRemove(this);
                        }
                    }
                };
                if (Array.isArray(disposables)) {
                    disposables.push(result);
                }
                return result;
            };
        }
        return this._event;
    }
    /**
     * To be kept private to fire an event to
     * subscribers
     */
    fire(event) {
        if (this._callbacks) {
            this._callbacks.invoke.call(this._callbacks, event);
        }
    }
    dispose() {
        if (this._callbacks) {
            this._callbacks.dispose();
            this._callbacks = undefined;
        }
    }
}
exports.Emitter = Emitter;
Emitter._noop = function () { };


/***/ }),

/***/ 78472:
/***/ ((__unused_webpack_module, exports) => {


/* --------------------------------------------------------------------------------------------
 * Copyright (c) Microsoft Corporation. All rights reserved.
 * Licensed under the MIT License. See License.txt in the project root for license information.
 * ------------------------------------------------------------------------------------------ */
Object.defineProperty(exports, "__esModule", ({ value: true }));
exports.stringArray = exports.array = exports.func = exports.error = exports.number = exports.string = exports.boolean = void 0;
function boolean(value) {
    return value === true || value === false;
}
exports.boolean = boolean;
function string(value) {
    return typeof value === 'string' || value instanceof String;
}
exports.string = string;
function number(value) {
    return typeof value === 'number' || value instanceof Number;
}
exports.number = number;
function error(value) {
    return value instanceof Error;
}
exports.error = error;
function func(value) {
    return typeof value === 'function';
}
exports.func = func;
function array(value) {
    return Array.isArray(value);
}
exports.array = array;
function stringArray(value) {
    return array(value) && value.every(elem => string(elem));
}
exports.stringArray = stringArray;


/***/ }),

/***/ 45164:
/***/ ((__unused_webpack_module, exports) => {


/*---------------------------------------------------------------------------------------------
 *  Copyright (c) Microsoft Corporation. All rights reserved.
 *  Licensed under the MIT License. See License.txt in the project root for license information.
 *--------------------------------------------------------------------------------------------*/
var _a;
Object.defineProperty(exports, "__esModule", ({ value: true }));
exports.LRUCache = exports.LinkedMap = exports.Touch = void 0;
var Touch;
(function (Touch) {
    Touch.None = 0;
    Touch.First = 1;
    Touch.AsOld = Touch.First;
    Touch.Last = 2;
    Touch.AsNew = Touch.Last;
})(Touch || (exports.Touch = Touch = {}));
class LinkedMap {
    constructor() {
        this[_a] = 'LinkedMap';
        this._map = new Map();
        this._head = undefined;
        this._tail = undefined;
        this._size = 0;
        this._state = 0;
    }
    clear() {
        this._map.clear();
        this._head = undefined;
        this._tail = undefined;
        this._size = 0;
        this._state++;
    }
    isEmpty() {
        return !this._head && !this._tail;
    }
    get size() {
        return this._size;
    }
    get first() {
        return this._head?.value;
    }
    get last() {
        return this._tail?.value;
    }
    has(key) {
        return this._map.has(key);
    }
    get(key, touch = Touch.None) {
        const item = this._map.get(key);
        if (!item) {
            return undefined;
        }
        if (touch !== Touch.None) {
            this.touch(item, touch);
        }
        return item.value;
    }
    set(key, value, touch = Touch.None) {
        let item = this._map.get(key);
        if (item) {
            item.value = value;
            if (touch !== Touch.None) {
                this.touch(item, touch);
            }
        }
        else {
            item = { key, value, next: undefined, previous: undefined };
            switch (touch) {
                case Touch.None:
                    this.addItemLast(item);
                    break;
                case Touch.First:
                    this.addItemFirst(item);
                    break;
                case Touch.Last:
                    this.addItemLast(item);
                    break;
                default:
                    this.addItemLast(item);
                    break;
            }
            this._map.set(key, item);
            this._size++;
        }
        return this;
    }
    delete(key) {
        return !!this.remove(key);
    }
    remove(key) {
        const item = this._map.get(key);
        if (!item) {
            return undefined;
        }
        this._map.delete(key);
        this.removeItem(item);
        this._size--;
        return item.value;
    }
    shift() {
        if (!this._head && !this._tail) {
            return undefined;
        }
        if (!this._head || !this._tail) {
            throw new Error('Invalid list');
        }
        const item = this._head;
        this._map.delete(item.key);
        this.removeItem(item);
        this._size--;
        return item.value;
    }
    forEach(callbackfn, thisArg) {
        const state = this._state;
        let current = this._head;
        while (current) {
            if (thisArg) {
                callbackfn.bind(thisArg)(current.value, current.key, this);
            }
            else {
                callbackfn(current.value, current.key, this);
            }
            if (this._state !== state) {
                throw new Error(`LinkedMap got modified during iteration.`);
            }
            current = current.next;
        }
    }
    keys() {
        const state = this._state;
        let current = this._head;
        const iterator = {
            [Symbol.iterator]: () => {
                return iterator;
            },
            next: () => {
                if (this._state !== state) {
                    throw new Error(`LinkedMap got modified during iteration.`);
                }
                if (current) {
                    const result = { value: current.key, done: false };
                    current = current.next;
                    return result;
                }
                else {
                    return { value: undefined, done: true };
                }
            }
        };
        return iterator;
    }
    values() {
        const state = this._state;
        let current = this._head;
        const iterator = {
            [Symbol.iterator]: () => {
                return iterator;
            },
            next: () => {
                if (this._state !== state) {
                    throw new Error(`LinkedMap got modified during iteration.`);
                }
                if (current) {
                    const result = { value: current.value, done: false };
                    current = current.next;
                    return result;
                }
                else {
                    return { value: undefined, done: true };
                }
            }
        };
        return iterator;
    }
    entries() {
        const state = this._state;
        let current = this._head;
        const iterator = {
            [Symbol.iterator]: () => {
                return iterator;
            },
            next: () => {
                if (this._state !== state) {
                    throw new Error(`LinkedMap got modified during iteration.`);
                }
                if (current) {
                    const result = { value: [current.key, current.value], done: false };
                    current = current.next;
                    return result;
                }
                else {
                    return { value: undefined, done: true };
                }
            }
        };
        return iterator;
    }
    [(_a = Symbol.toStringTag, Symbol.iterator)]() {
        return this.entries();
    }
    trimOld(newSize) {
        if (newSize >= this.size) {
            return;
        }
        if (newSize === 0) {
            this.clear();
            return;
        }
        let current = this._head;
        let currentSize = this.size;
        while (current && currentSize > newSize) {
            this._map.delete(current.key);
            current = current.next;
            currentSize--;
        }
        this._head = current;
        this._size = currentSize;
        if (current) {
            current.previous = undefined;
        }
        this._state++;
    }
    addItemFirst(item) {
        // First time Insert
        if (!this._head && !this._tail) {
            this._tail = item;
        }
        else if (!this._head) {
            throw new Error('Invalid list');
        }
        else {
            item.next = this._head;
            this._head.previous = item;
        }
        this._head = item;
        this._state++;
    }
    addItemLast(item) {
        // First time Insert
        if (!this._head && !this._tail) {
            this._head = item;
        }
        else if (!this._tail) {
            throw new Error('Invalid list');
        }
        else {
            item.previous = this._tail;
            this._tail.next = item;
        }
        this._tail = item;
        this._state++;
    }
    removeItem(item) {
        if (item === this._head && item === this._tail) {
            this._head = undefined;
            this._tail = undefined;
        }
        else if (item === this._head) {
            // This can only happened if size === 1 which is handle
            // by the case above.
            if (!item.next) {
                throw new Error('Invalid list');
            }
            item.next.previous = undefined;
            this._head = item.next;
        }
        else if (item === this._tail) {
            // This can only happened if size === 1 which is handle
            // by the case above.
            if (!item.previous) {
                throw new Error('Invalid list');
            }
            item.previous.next = undefined;
            this._tail = item.previous;
        }
        else {
            const next = item.next;
            const previous = item.previous;
            if (!next || !previous) {
                throw new Error('Invalid list');
            }
            next.previous = previous;
            previous.next = next;
        }
        item.next = undefined;
        item.previous = undefined;
        this._state++;
    }
    touch(item, touch) {
        if (!this._head || !this._tail) {
            throw new Error('Invalid list');
        }
        if ((touch !== Touch.First && touch !== Touch.Last)) {
            return;
        }
        if (touch === Touch.First) {
            if (item === this._head) {
                return;
            }
            const next = item.next;
            const previous = item.previous;
            // Unlink the item
            if (item === this._tail) {
                // previous must be defined since item was not head but is tail
                // So there are more than on item in the map
                previous.next = undefined;
                this._tail = previous;
            }
            else {
                // Both next and previous are not undefined since item was neither head nor tail.
                next.previous = previous;
                previous.next = next;
            }
            // Insert the node at head
            item.previous = undefined;
            item.next = this._head;
            this._head.previous = item;
            this._head = item;
            this._state++;
        }
        else if (touch === Touch.Last) {
            if (item === this._tail) {
                return;
            }
            const next = item.next;
            const previous = item.previous;
            // Unlink the item.
            if (item === this._head) {
                // next must be defined since item was not tail but is head
                // So there are more than on item in the map
                next.previous = undefined;
                this._head = next;
            }
            else {
                // Both next and previous are not undefined since item was neither head nor tail.
                next.previous = previous;
                previous.next = next;
            }
            item.next = undefined;
            item.previous = this._tail;
            this._tail.next = item;
            this._tail = item;
            this._state++;
        }
    }
    toJSON() {
        const data = [];
        this.forEach((value, key) => {
            data.push([key, value]);
        });
        return data;
    }
    fromJSON(data) {
        this.clear();
        for (const [key, value] of data) {
            this.set(key, value);
        }
    }
}
exports.LinkedMap = LinkedMap;
class LRUCache extends LinkedMap {
    constructor(limit, ratio = 1) {
        super();
        this._limit = limit;
        this._ratio = Math.min(Math.max(0, ratio), 1);
    }
    get limit() {
        return this._limit;
    }
    set limit(limit) {
        this._limit = limit;
        this.checkTrim();
    }
    get ratio() {
        return this._ratio;
    }
    set ratio(ratio) {
        this._ratio = Math.min(Math.max(0, ratio), 1);
        this.checkTrim();
    }
    get(key, touch = Touch.AsNew) {
        return super.get(key, touch);
    }
    peek(key) {
        return super.get(key, Touch.None);
    }
    set(key, value) {
        super.set(key, value, Touch.Last);
        this.checkTrim();
        return this;
    }
    checkTrim() {
        if (this.size > this._limit) {
            this.trimOld(Math.round(this._limit * this._ratio));
        }
    }
}
exports.LRUCache = LRUCache;


/***/ }),

/***/ 15506:
/***/ ((__unused_webpack_module, exports) => {


/*---------------------------------------------------------------------------------------------
 *  Copyright (c) Microsoft Corporation. All rights reserved.
 *  Licensed under the MIT License. See License.txt in the project root for license information.
 *--------------------------------------------------------------------------------------------*/
Object.defineProperty(exports, "__esModule", ({ value: true }));
exports.AbstractMessageBuffer = void 0;
const CR = 13;
const LF = 10;
const CRLF = '\r\n';
class AbstractMessageBuffer {
    constructor(encoding = 'utf-8') {
        this._encoding = encoding;
        this._chunks = [];
        this._totalLength = 0;
    }
    get encoding() {
        return this._encoding;
    }
    append(chunk) {
        const toAppend = typeof chunk === 'string' ? this.fromString(chunk, this._encoding) : chunk;
        this._chunks.push(toAppend);
        this._totalLength += toAppend.byteLength;
    }
    tryReadHeaders(lowerCaseKeys = false) {
        if (this._chunks.length === 0) {
            return undefined;
        }
        let state = 0;
        let chunkIndex = 0;
        let offset = 0;
        let chunkBytesRead = 0;
        row: while (chunkIndex < this._chunks.length) {
            const chunk = this._chunks[chunkIndex];
            offset = 0;
            column: while (offset < chunk.length) {
                const value = chunk[offset];
                switch (value) {
                    case CR:
                        switch (state) {
                            case 0:
                                state = 1;
                                break;
                            case 2:
                                state = 3;
                                break;
                            default:
                                state = 0;
                        }
                        break;
                    case LF:
                        switch (state) {
                            case 1:
                                state = 2;
                                break;
                            case 3:
                                state = 4;
                                offset++;
                                break row;
                            default:
                                state = 0;
                        }
                        break;
                    default:
                        state = 0;
                }
                offset++;
            }
            chunkBytesRead += chunk.byteLength;
            chunkIndex++;
        }
        if (state !== 4) {
            return undefined;
        }
        // The buffer contains the two CRLF at the end. So we will
        // have two empty lines after the split at the end as well.
        const buffer = this._read(chunkBytesRead + offset);
        const result = new Map();
        const headers = this.toString(buffer, 'ascii').split(CRLF);
        if (headers.length < 2) {
            return result;
        }
        for (let i = 0; i < headers.length - 2; i++) {
            const header = headers[i];
            const index = header.indexOf(':');
            if (index === -1) {
                throw new Error(`Message header must separate key and value using ':'\n${header}`);
            }
            const key = header.substr(0, index);
            const value = header.substr(index + 1).trim();
            result.set(lowerCaseKeys ? key.toLowerCase() : key, value);
        }
        return result;
    }
    tryReadBody(length) {
        if (this._totalLength < length) {
            return undefined;
        }
        return this._read(length);
    }
    get numberOfBytes() {
        return this._totalLength;
    }
    _read(byteCount) {
        if (byteCount === 0) {
            return this.emptyBuffer();
        }
        if (byteCount > this._totalLength) {
            throw new Error(`Cannot read so many bytes!`);
        }
        if (this._chunks[0].byteLength === byteCount) {
            // super fast path, precisely first chunk must be returned
            const chunk = this._chunks[0];
            this._chunks.shift();
            this._totalLength -= byteCount;
            return this.asNative(chunk);
        }
        if (this._chunks[0].byteLength > byteCount) {
            // fast path, the reading is entirely within the first chunk
            const chunk = this._chunks[0];
            const result = this.asNative(chunk, byteCount);
            this._chunks[0] = chunk.slice(byteCount);
            this._totalLength -= byteCount;
            return result;
        }
        const result = this.allocNative(byteCount);
        let resultOffset = 0;
        let chunkIndex = 0;
        while (byteCount > 0) {
            const chunk = this._chunks[chunkIndex];
            if (chunk.byteLength > byteCount) {
                // this chunk will survive
                const chunkPart = chunk.slice(0, byteCount);
                result.set(chunkPart, resultOffset);
                resultOffset += byteCount;
                this._chunks[chunkIndex] = chunk.slice(byteCount);
                this._totalLength -= byteCount;
                byteCount -= byteCount;
            }
            else {
                // this chunk will be entirely read
                result.set(chunk, resultOffset);
                resultOffset += chunk.byteLength;
                this._chunks.shift();
                this._totalLength -= chunk.byteLength;
                byteCount -= chunk.byteLength;
            }
        }
        return result;
    }
}
exports.AbstractMessageBuffer = AbstractMessageBuffer;


/***/ }),

/***/ 84806:
/***/ ((__unused_webpack_module, exports, __webpack_require__) => {


/* --------------------------------------------------------------------------------------------
 * Copyright (c) Microsoft Corporation. All rights reserved.
 * Licensed under the MIT License. See License.txt in the project root for license information.
 * ------------------------------------------------------------------------------------------ */
Object.defineProperty(exports, "__esModule", ({ value: true }));
exports.ReadableStreamMessageReader = exports.AbstractMessageReader = exports.MessageReader = void 0;
const ral_1 = __webpack_require__(48094);
const Is = __webpack_require__(78472);
const events_1 = __webpack_require__(345);
const semaphore_1 = __webpack_require__(86791);
var MessageReader;
(function (MessageReader) {
    function is(value) {
        let candidate = value;
        return candidate && Is.func(candidate.listen) && Is.func(candidate.dispose) &&
            Is.func(candidate.onError) && Is.func(candidate.onClose) && Is.func(candidate.onPartialMessage);
    }
    MessageReader.is = is;
})(MessageReader || (exports.MessageReader = MessageReader = {}));
class AbstractMessageReader {
    constructor() {
        this.errorEmitter = new events_1.Emitter();
        this.closeEmitter = new events_1.Emitter();
        this.partialMessageEmitter = new events_1.Emitter();
    }
    dispose() {
        this.errorEmitter.dispose();
        this.closeEmitter.dispose();
    }
    get onError() {
        return this.errorEmitter.event;
    }
    fireError(error) {
        this.errorEmitter.fire(this.asError(error));
    }
    get onClose() {
        return this.closeEmitter.event;
    }
    fireClose() {
        this.closeEmitter.fire(undefined);
    }
    get onPartialMessage() {
        return this.partialMessageEmitter.event;
    }
    firePartialMessage(info) {
        this.partialMessageEmitter.fire(info);
    }
    asError(error) {
        if (error instanceof Error) {
            return error;
        }
        else {
            return new Error(`Reader received error. Reason: ${Is.string(error.message) ? error.message : 'unknown'}`);
        }
    }
}
exports.AbstractMessageReader = AbstractMessageReader;
var ResolvedMessageReaderOptions;
(function (ResolvedMessageReaderOptions) {
    function fromOptions(options) {
        let charset;
        let result;
        let contentDecoder;
        const contentDecoders = new Map();
        let contentTypeDecoder;
        const contentTypeDecoders = new Map();
        if (options === undefined || typeof options === 'string') {
            charset = options ?? 'utf-8';
        }
        else {
            charset = options.charset ?? 'utf-8';
            if (options.contentDecoder !== undefined) {
                contentDecoder = options.contentDecoder;
                contentDecoders.set(contentDecoder.name, contentDecoder);
            }
            if (options.contentDecoders !== undefined) {
                for (const decoder of options.contentDecoders) {
                    contentDecoders.set(decoder.name, decoder);
                }
            }
            if (options.contentTypeDecoder !== undefined) {
                contentTypeDecoder = options.contentTypeDecoder;
                contentTypeDecoders.set(contentTypeDecoder.name, contentTypeDecoder);
            }
            if (options.contentTypeDecoders !== undefined) {
                for (const decoder of options.contentTypeDecoders) {
                    contentTypeDecoders.set(decoder.name, decoder);
                }
            }
        }
        if (contentTypeDecoder === undefined) {
            contentTypeDecoder = (0, ral_1.default)().applicationJson.decoder;
            contentTypeDecoders.set(contentTypeDecoder.name, contentTypeDecoder);
        }
        return { charset, contentDecoder, contentDecoders, contentTypeDecoder, contentTypeDecoders };
    }
    ResolvedMessageReaderOptions.fromOptions = fromOptions;
})(ResolvedMessageReaderOptions || (ResolvedMessageReaderOptions = {}));
class ReadableStreamMessageReader extends AbstractMessageReader {
    constructor(readable, options) {
        super();
        this.readable = readable;
        this.options = ResolvedMessageReaderOptions.fromOptions(options);
        this.buffer = (0, ral_1.default)().messageBuffer.create(this.options.charset);
        this._partialMessageTimeout = 10000;
        this.nextMessageLength = -1;
        this.messageToken = 0;
        this.readSemaphore = new semaphore_1.Semaphore(1);
    }
    set partialMessageTimeout(timeout) {
        this._partialMessageTimeout = timeout;
    }
    get partialMessageTimeout() {
        return this._partialMessageTimeout;
    }
    listen(callback) {
        this.nextMessageLength = -1;
        this.messageToken = 0;
        this.partialMessageTimer = undefined;
        this.callback = callback;
        const result = this.readable.onData((data) => {
            this.onData(data);
        });
        this.readable.onError((error) => this.fireError(error));
        this.readable.onClose(() => this.fireClose());
        return result;
    }
    onData(data) {
        try {
            this.buffer.append(data);
            while (true) {
                if (this.nextMessageLength === -1) {
                    const headers = this.buffer.tryReadHeaders(true);
                    if (!headers) {
                        return;
                    }
                    const contentLength = headers.get('content-length');
                    if (!contentLength) {
                        this.fireError(new Error(`Header must provide a Content-Length property.\n${JSON.stringify(Object.fromEntries(headers))}`));
                        return;
                    }
                    const length = parseInt(contentLength);
                    if (isNaN(length)) {
                        this.fireError(new Error(`Content-Length value must be a number. Got ${contentLength}`));
                        return;
                    }
                    this.nextMessageLength = length;
                }
                const body = this.buffer.tryReadBody(this.nextMessageLength);
                if (body === undefined) {
                    /** We haven't received the full message yet. */
                    this.setPartialMessageTimer();
                    return;
                }
                this.clearPartialMessageTimer();
                this.nextMessageLength = -1;
                // Make sure that we convert one received message after the
                // other. Otherwise it could happen that a decoding of a second
                // smaller message finished before the decoding of a first larger
                // message and then we would deliver the second message first.
                this.readSemaphore.lock(async () => {
                    const bytes = this.options.contentDecoder !== undefined
                        ? await this.options.contentDecoder.decode(body)
                        : body;
                    const message = await this.options.contentTypeDecoder.decode(bytes, this.options);
                    this.callback(message);
                }).catch((error) => {
                    this.fireError(error);
                });
            }
        }
        catch (error) {
            this.fireError(error);
        }
    }
    clearPartialMessageTimer() {
        if (this.partialMessageTimer) {
            this.partialMessageTimer.dispose();
            this.partialMessageTimer = undefined;
        }
    }
    setPartialMessageTimer() {
        this.clearPartialMessageTimer();
        if (this._partialMessageTimeout <= 0) {
            return;
        }
        this.partialMessageTimer = (0, ral_1.default)().timer.setTimeout((token, timeout) => {
            this.partialMessageTimer = undefined;
            if (token === this.messageToken) {
                this.firePartialMessage({ messageToken: token, waitingTime: timeout });
                this.setPartialMessageTimer();
            }
        }, this._partialMessageTimeout, this.messageToken, this._partialMessageTimeout);
    }
}
exports.ReadableStreamMessageReader = ReadableStreamMessageReader;


/***/ }),

/***/ 69248:
/***/ ((__unused_webpack_module, exports, __webpack_require__) => {


/* --------------------------------------------------------------------------------------------
 * Copyright (c) Microsoft Corporation. All rights reserved.
 * Licensed under the MIT License. See License.txt in the project root for license information.
 * ------------------------------------------------------------------------------------------ */
Object.defineProperty(exports, "__esModule", ({ value: true }));
exports.WriteableStreamMessageWriter = exports.AbstractMessageWriter = exports.MessageWriter = void 0;
const ral_1 = __webpack_require__(48094);
const Is = __webpack_require__(78472);
const semaphore_1 = __webpack_require__(86791);
const events_1 = __webpack_require__(345);
const ContentLength = 'Content-Length: ';
const CRLF = '\r\n';
var MessageWriter;
(function (MessageWriter) {
    function is(value) {
        let candidate = value;
        return candidate && Is.func(candidate.dispose) && Is.func(candidate.onClose) &&
            Is.func(candidate.onError) && Is.func(candidate.write);
    }
    MessageWriter.is = is;
})(MessageWriter || (exports.MessageWriter = MessageWriter = {}));
class AbstractMessageWriter {
    constructor() {
        this.errorEmitter = new events_1.Emitter();
        this.closeEmitter = new events_1.Emitter();
    }
    dispose() {
        this.errorEmitter.dispose();
        this.closeEmitter.dispose();
    }
    get onError() {
        return this.errorEmitter.event;
    }
    fireError(error, message, count) {
        this.errorEmitter.fire([this.asError(error), message, count]);
    }
    get onClose() {
        return this.closeEmitter.event;
    }
    fireClose() {
        this.closeEmitter.fire(undefined);
    }
    asError(error) {
        if (error instanceof Error) {
            return error;
        }
        else {
            return new Error(`Writer received error. Reason: ${Is.string(error.message) ? error.message : 'unknown'}`);
        }
    }
}
exports.AbstractMessageWriter = AbstractMessageWriter;
var ResolvedMessageWriterOptions;
(function (ResolvedMessageWriterOptions) {
    function fromOptions(options) {
        if (options === undefined || typeof options === 'string') {
            return { charset: options ?? 'utf-8', contentTypeEncoder: (0, ral_1.default)().applicationJson.encoder };
        }
        else {
            return { charset: options.charset ?? 'utf-8', contentEncoder: options.contentEncoder, contentTypeEncoder: options.contentTypeEncoder ?? (0, ral_1.default)().applicationJson.encoder };
        }
    }
    ResolvedMessageWriterOptions.fromOptions = fromOptions;
})(ResolvedMessageWriterOptions || (ResolvedMessageWriterOptions = {}));
class WriteableStreamMessageWriter extends AbstractMessageWriter {
    constructor(writable, options) {
        super();
        this.writable = writable;
        this.options = ResolvedMessageWriterOptions.fromOptions(options);
        this.errorCount = 0;
        this.writeSemaphore = new semaphore_1.Semaphore(1);
        this.writable.onError((error) => this.fireError(error));
        this.writable.onClose(() => this.fireClose());
    }
    async write(msg) {
        return this.writeSemaphore.lock(async () => {
            const payload = this.options.contentTypeEncoder.encode(msg, this.options).then((buffer) => {
                if (this.options.contentEncoder !== undefined) {
                    return this.options.contentEncoder.encode(buffer);
                }
                else {
                    return buffer;
                }
            });
            return payload.then((buffer) => {
                const headers = [];
                headers.push(ContentLength, buffer.byteLength.toString(), CRLF);
                headers.push(CRLF);
                return this.doWrite(msg, headers, buffer);
            }, (error) => {
                this.fireError(error);
                throw error;
            });
        });
    }
    async doWrite(msg, headers, data) {
        try {
            await this.writable.write(headers.join(''), 'ascii');
            return this.writable.write(data);
        }
        catch (error) {
            this.handleError(error, msg);
            return Promise.reject(error);
        }
    }
    handleError(error, msg) {
        this.errorCount++;
        this.fireError(error, msg, this.errorCount);
    }
    end() {
        this.writable.end();
    }
}
exports.WriteableStreamMessageWriter = WriteableStreamMessageWriter;


/***/ }),

/***/ 75285:
/***/ ((__unused_webpack_module, exports, __webpack_require__) => {


/* --------------------------------------------------------------------------------------------
 * Copyright (c) Microsoft Corporation. All rights reserved.
 * Licensed under the MIT License. See License.txt in the project root for license information.
 * ------------------------------------------------------------------------------------------ */
Object.defineProperty(exports, "__esModule", ({ value: true }));
exports.Message = exports.NotificationType9 = exports.NotificationType8 = exports.NotificationType7 = exports.NotificationType6 = exports.NotificationType5 = exports.NotificationType4 = exports.NotificationType3 = exports.NotificationType2 = exports.NotificationType1 = exports.NotificationType0 = exports.NotificationType = exports.RequestType9 = exports.RequestType8 = exports.RequestType7 = exports.RequestType6 = exports.RequestType5 = exports.RequestType4 = exports.RequestType3 = exports.RequestType2 = exports.RequestType1 = exports.RequestType = exports.RequestType0 = exports.AbstractMessageSignature = exports.ParameterStructures = exports.ResponseError = exports.ErrorCodes = void 0;
const is = __webpack_require__(78472);
/**
 * Predefined error codes.
 */
var ErrorCodes;
(function (ErrorCodes) {
    // Defined by JSON RPC
    ErrorCodes.ParseError = -32700;
    ErrorCodes.InvalidRequest = -32600;
    ErrorCodes.MethodNotFound = -32601;
    ErrorCodes.InvalidParams = -32602;
    ErrorCodes.InternalError = -32603;
    /**
     * This is the start range of JSON RPC reserved error codes.
     * It doesn't denote a real error code. No application error codes should
     * be defined between the start and end range. For backwards
     * compatibility the `ServerNotInitialized` and the `UnknownErrorCode`
     * are left in the range.
     *
     * @since 3.16.0
    */
    ErrorCodes.jsonrpcReservedErrorRangeStart = -32099;
    /** @deprecated use  jsonrpcReservedErrorRangeStart */
    ErrorCodes.serverErrorStart = -32099;
    /**
     * An error occurred when write a message to the transport layer.
     */
    ErrorCodes.MessageWriteError = -32099;
    /**
     * An error occurred when reading a message from the transport layer.
     */
    ErrorCodes.MessageReadError = -32098;
    /**
     * The connection got disposed or lost and all pending responses got
     * rejected.
     */
    ErrorCodes.PendingResponseRejected = -32097;
    /**
     * The connection is inactive and a use of it failed.
     */
    ErrorCodes.ConnectionInactive = -32096;
    /**
     * Error code indicating that a server received a notification or
     * request before the server has received the `initialize` request.
     */
    ErrorCodes.ServerNotInitialized = -32002;
    ErrorCodes.UnknownErrorCode = -32001;
    /**
     * This is the end range of JSON RPC reserved error codes.
     * It doesn't denote a real error code.
     *
     * @since 3.16.0
    */
    ErrorCodes.jsonrpcReservedErrorRangeEnd = -32000;
    /** @deprecated use  jsonrpcReservedErrorRangeEnd */
    ErrorCodes.serverErrorEnd = -32000;
})(ErrorCodes || (exports.ErrorCodes = ErrorCodes = {}));
/**
 * An error object return in a response in case a request
 * has failed.
 */
class ResponseError extends Error {
    constructor(code, message, data) {
        super(message);
        this.code = is.number(code) ? code : ErrorCodes.UnknownErrorCode;
        this.data = data;
        Object.setPrototypeOf(this, ResponseError.prototype);
    }
    toJson() {
        const result = {
            code: this.code,
            message: this.message
        };
        if (this.data !== undefined) {
            result.data = this.data;
        }
        return result;
    }
}
exports.ResponseError = ResponseError;
class ParameterStructures {
    constructor(kind) {
        this.kind = kind;
    }
    static is(value) {
        return value === ParameterStructures.auto || value === ParameterStructures.byName || value === ParameterStructures.byPosition;
    }
    toString() {
        return this.kind;
    }
}
exports.ParameterStructures = ParameterStructures;
/**
 * The parameter structure is automatically inferred on the number of parameters
 * and the parameter type in case of a single param.
 */
ParameterStructures.auto = new ParameterStructures('auto');
/**
 * Forces `byPosition` parameter structure. This is useful if you have a single
 * parameter which has a literal type.
 */
ParameterStructures.byPosition = new ParameterStructures('byPosition');
/**
 * Forces `byName` parameter structure. This is only useful when having a single
 * parameter. The library will report errors if used with a different number of
 * parameters.
 */
ParameterStructures.byName = new ParameterStructures('byName');
/**
 * An abstract implementation of a MessageType.
 */
class AbstractMessageSignature {
    constructor(method, numberOfParams) {
        this.method = method;
        this.numberOfParams = numberOfParams;
    }
    get parameterStructures() {
        return ParameterStructures.auto;
    }
}
exports.AbstractMessageSignature = AbstractMessageSignature;
/**
 * Classes to type request response pairs
 */
class RequestType0 extends AbstractMessageSignature {
    constructor(method) {
        super(method, 0);
    }
}
exports.RequestType0 = RequestType0;
class RequestType extends AbstractMessageSignature {
    constructor(method, _parameterStructures = ParameterStructures.auto) {
        super(method, 1);
        this._parameterStructures = _parameterStructures;
    }
    get parameterStructures() {
        return this._parameterStructures;
    }
}
exports.RequestType = RequestType;
class RequestType1 extends AbstractMessageSignature {
    constructor(method, _parameterStructures = ParameterStructures.auto) {
        super(method, 1);
        this._parameterStructures = _parameterStructures;
    }
    get parameterStructures() {
        return this._parameterStructures;
    }
}
exports.RequestType1 = RequestType1;
class RequestType2 extends AbstractMessageSignature {
    constructor(method) {
        super(method, 2);
    }
}
exports.RequestType2 = RequestType2;
class RequestType3 extends AbstractMessageSignature {
    constructor(method) {
        super(method, 3);
    }
}
exports.RequestType3 = RequestType3;
class RequestType4 extends AbstractMessageSignature {
    constructor(method) {
        super(method, 4);
    }
}
exports.RequestType4 = RequestType4;
class RequestType5 extends AbstractMessageSignature {
    constructor(method) {
        super(method, 5);
    }
}
exports.RequestType5 = RequestType5;
class RequestType6 extends AbstractMessageSignature {
    constructor(method) {
        super(method, 6);
    }
}
exports.RequestType6 = RequestType6;
class RequestType7 extends AbstractMessageSignature {
    constructor(method) {
        super(method, 7);
    }
}
exports.RequestType7 = RequestType7;
class RequestType8 extends AbstractMessageSignature {
    constructor(method) {
        super(method, 8);
    }
}
exports.RequestType8 = RequestType8;
class RequestType9 extends AbstractMessageSignature {
    constructor(method) {
        super(method, 9);
    }
}
exports.RequestType9 = RequestType9;
class NotificationType extends AbstractMessageSignature {
    constructor(method, _parameterStructures = ParameterStructures.auto) {
        super(method, 1);
        this._parameterStructures = _parameterStructures;
    }
    get parameterStructures() {
        return this._parameterStructures;
    }
}
exports.NotificationType = NotificationType;
class NotificationType0 extends AbstractMessageSignature {
    constructor(method) {
        super(method, 0);
    }
}
exports.NotificationType0 = NotificationType0;
class NotificationType1 extends AbstractMessageSignature {
    constructor(method, _parameterStructures = ParameterStructures.auto) {
        super(method, 1);
        this._parameterStructures = _parameterStructures;
    }
    get parameterStructures() {
        return this._parameterStructures;
    }
}
exports.NotificationType1 = NotificationType1;
class NotificationType2 extends AbstractMessageSignature {
    constructor(method) {
        super(method, 2);
    }
}
exports.NotificationType2 = NotificationType2;
class NotificationType3 extends AbstractMessageSignature {
    constructor(method) {
        super(method, 3);
    }
}
exports.NotificationType3 = NotificationType3;
class NotificationType4 extends AbstractMessageSignature {
    constructor(method) {
        super(method, 4);
    }
}
exports.NotificationType4 = NotificationType4;
class NotificationType5 extends AbstractMessageSignature {
    constructor(method) {
        super(method, 5);
    }
}
exports.NotificationType5 = NotificationType5;
class NotificationType6 extends AbstractMessageSignature {
    constructor(method) {
        super(method, 6);
    }
}
exports.NotificationType6 = NotificationType6;
class NotificationType7 extends AbstractMessageSignature {
    constructor(method) {
        super(method, 7);
    }
}
exports.NotificationType7 = NotificationType7;
class NotificationType8 extends AbstractMessageSignature {
    constructor(method) {
        super(method, 8);
    }
}
exports.NotificationType8 = NotificationType8;
class NotificationType9 extends AbstractMessageSignature {
    constructor(method) {
        super(method, 9);
    }
}
exports.NotificationType9 = NotificationType9;
var Message;
(function (Message) {
    /**
     * Tests if the given message is a request message
     */
    function isRequest(message) {
        const candidate = message;
        return candidate && is.string(candidate.method) && (is.string(candidate.id) || is.number(candidate.id));
    }
    Message.isRequest = isRequest;
    /**
     * Tests if the given message is a notification message
     */
    function isNotification(message) {
        const candidate = message;
        return candidate && is.string(candidate.method) && message.id === void 0;
    }
    Message.isNotification = isNotification;
    /**
     * Tests if the given message is a response message
     */
    function isResponse(message) {
        const candidate = message;
        return candidate && (candidate.result !== void 0 || !!candidate.error) && (is.string(candidate.id) || is.number(candidate.id) || candidate.id === null);
    }
    Message.isResponse = isResponse;
})(Message || (exports.Message = Message = {}));


/***/ }),

/***/ 48094:
/***/ ((__unused_webpack_module, exports) => {


/* --------------------------------------------------------------------------------------------
 * Copyright (c) Microsoft Corporation. All rights reserved.
 * Licensed under the MIT License. See License.txt in the project root for license information.
 * ------------------------------------------------------------------------------------------ */
Object.defineProperty(exports, "__esModule", ({ value: true }));
let _ral;
function RAL() {
    if (_ral === undefined) {
        throw new Error(`No runtime abstraction layer installed`);
    }
    return _ral;
}
(function (RAL) {
    function install(ral) {
        if (ral === undefined) {
            throw new Error(`No runtime abstraction layer provided`);
        }
        _ral = ral;
    }
    RAL.install = install;
})(RAL || (RAL = {}));
exports["default"] = RAL;


/***/ }),

/***/ 86791:
/***/ ((__unused_webpack_module, exports, __webpack_require__) => {


/* --------------------------------------------------------------------------------------------
 * Copyright (c) Microsoft Corporation. All rights reserved.
 * Licensed under the MIT License. See License.txt in the project root for license information.
 * ------------------------------------------------------------------------------------------ */
Object.defineProperty(exports, "__esModule", ({ value: true }));
exports.Semaphore = void 0;
const ral_1 = __webpack_require__(48094);
class Semaphore {
    constructor(capacity = 1) {
        if (capacity <= 0) {
            throw new Error('Capacity must be greater than 0');
        }
        this._capacity = capacity;
        this._active = 0;
        this._waiting = [];
    }
    lock(thunk) {
        return new Promise((resolve, reject) => {
            this._waiting.push({ thunk, resolve, reject });
            this.runNext();
        });
    }
    get active() {
        return this._active;
    }
    runNext() {
        if (this._waiting.length === 0 || this._active === this._capacity) {
            return;
        }
        (0, ral_1.default)().timer.setImmediate(() => this.doRunNext());
    }
    doRunNext() {
        if (this._waiting.length === 0 || this._active === this._capacity) {
            return;
        }
        const next = this._waiting.shift();
        this._active++;
        if (this._active > this._capacity) {
            throw new Error(`To many thunks active`);
        }
        try {
            const result = next.thunk();
            if (result instanceof Promise) {
                result.then((value) => {
                    this._active--;
                    next.resolve(value);
                    this.runNext();
                }, (err) => {
                    this._active--;
                    next.reject(err);
                    this.runNext();
                });
            }
            else {
                this._active--;
                next.resolve(result);
                this.runNext();
            }
        }
        catch (err) {
            this._active--;
            next.reject(err);
            this.runNext();
        }
    }
}
exports.Semaphore = Semaphore;


/***/ }),

/***/ 50278:
/***/ ((__unused_webpack_module, exports, __webpack_require__) => {


/* --------------------------------------------------------------------------------------------
 * Copyright (c) Microsoft Corporation. All rights reserved.
 * Licensed under the MIT License. See License.txt in the project root for license information.
 * ------------------------------------------------------------------------------------------ */
Object.defineProperty(exports, "__esModule", ({ value: true }));
exports.SharedArrayReceiverStrategy = exports.SharedArraySenderStrategy = void 0;
const cancellation_1 = __webpack_require__(97770);
var CancellationState;
(function (CancellationState) {
    CancellationState.Continue = 0;
    CancellationState.Cancelled = 1;
})(CancellationState || (CancellationState = {}));
class SharedArraySenderStrategy {
    constructor() {
        this.buffers = new Map();
    }
    enableCancellation(request) {
        if (request.id === null) {
            return;
        }
        const buffer = new SharedArrayBuffer(4);
        const data = new Int32Array(buffer, 0, 1);
        data[0] = CancellationState.Continue;
        this.buffers.set(request.id, buffer);
        request.$cancellationData = buffer;
    }
    async sendCancellation(_conn, id) {
        const buffer = this.buffers.get(id);
        if (buffer === undefined) {
            return;
        }
        const data = new Int32Array(buffer, 0, 1);
        Atomics.store(data, 0, CancellationState.Cancelled);
    }
    cleanup(id) {
        this.buffers.delete(id);
    }
    dispose() {
        this.buffers.clear();
    }
}
exports.SharedArraySenderStrategy = SharedArraySenderStrategy;
class SharedArrayBufferCancellationToken {
    constructor(buffer) {
        this.data = new Int32Array(buffer, 0, 1);
    }
    get isCancellationRequested() {
        return Atomics.load(this.data, 0) === CancellationState.Cancelled;
    }
    get onCancellationRequested() {
        throw new Error(`Cancellation over SharedArrayBuffer doesn't support cancellation events`);
    }
}
class SharedArrayBufferCancellationTokenSource {
    constructor(buffer) {
        this.token = new SharedArrayBufferCancellationToken(buffer);
    }
    cancel() {
    }
    dispose() {
    }
}
class SharedArrayReceiverStrategy {
    constructor() {
        this.kind = 'request';
    }
    createCancellationTokenSource(request) {
        const buffer = request.$cancellationData;
        if (buffer === undefined) {
            return new cancellation_1.CancellationTokenSource();
        }
        return new SharedArrayBufferCancellationTokenSource(buffer);
    }
}
exports.SharedArrayReceiverStrategy = SharedArrayReceiverStrategy;


/***/ })

}]);
//# sourceMappingURL=9406.e7b7cac175c969aeda34.js.map?v=e7b7cac175c969aeda34