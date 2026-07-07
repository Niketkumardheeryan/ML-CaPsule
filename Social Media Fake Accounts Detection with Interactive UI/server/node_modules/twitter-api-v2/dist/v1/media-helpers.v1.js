"use strict";
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
var __setModuleDefault = (this && this.__setModuleDefault) || (Object.create ? (function(o, v) {
    Object.defineProperty(o, "default", { enumerable: true, value: v });
}) : function(o, v) {
    o["default"] = v;
});
var __importStar = (this && this.__importStar) || function (mod) {
    if (mod && mod.__esModule) return mod;
    var result = {};
    if (mod != null) for (var k in mod) if (k !== "default" && Object.prototype.hasOwnProperty.call(mod, k)) __createBinding(result, mod, k);
    __setModuleDefault(result, mod);
    return result;
};
Object.defineProperty(exports, "__esModule", { value: true });
exports.readNextPartOf = exports.sleepSecs = exports.getMediaCategoryByMime = exports.getMimeType = exports.getFileSizeFromFileHandle = exports.getFileHandle = exports.readFileIntoBuffer = void 0;
const fs = __importStar(require("fs"));
const helpers_1 = require("../helpers");
const types_1 = require("../types");
async function readFileIntoBuffer(file) {
    const handle = await getFileHandle(file);
    if (typeof handle === 'number') {
        return new Promise((resolve, reject) => {
            fs.readFile(handle, (err, data) => {
                if (err) {
                    return reject(err);
                }
                resolve(data);
            });
        });
    }
    else if (handle instanceof Buffer) {
        return handle;
    }
    else {
        return handle.readFile();
    }
}
exports.readFileIntoBuffer = readFileIntoBuffer;
function getFileHandle(file) {
    if (typeof file === 'string') {
        return fs.promises.open(file, 'r');
    }
    else if (typeof file === 'number') {
        return file;
    }
    else if (typeof file === 'object' && !(file instanceof Buffer)) {
        return file;
    }
    else if (!(file instanceof Buffer)) {
        throw new Error('Given file is not valid, please check its type.');
    }
    else {
        return file;
    }
}
exports.getFileHandle = getFileHandle;
async function getFileSizeFromFileHandle(fileHandle) {
    // Get the file size
    if (typeof fileHandle === 'number') {
        const stats = await new Promise((resolve, reject) => {
            fs.fstat(fileHandle, (err, stats) => {
                if (err)
                    reject(err);
                resolve(stats);
            });
        });
        return stats.size;
    }
    else if (fileHandle instanceof Buffer) {
        return fileHandle.length;
    }
    else {
        return (await fileHandle.stat()).size;
    }
}
exports.getFileSizeFromFileHandle = getFileSizeFromFileHandle;
function getMimeType(file, type, mimeType) {
    if (typeof mimeType === 'string') {
        return mimeType;
    }
    else if (typeof file === 'string' && !type) {
        return getMimeByName(file);
    }
    else if (typeof type === 'string') {
        return getMimeByType(type);
    }
    throw new Error('You must specify type if file is a file handle or Buffer.');
}
exports.getMimeType = getMimeType;
function getMimeByName(name) {
    if (name.endsWith('.jpeg') || name.endsWith('.jpg'))
        return types_1.EUploadMimeType.Jpeg;
    if (name.endsWith('.png'))
        return types_1.EUploadMimeType.Png;
    if (name.endsWith('.webp'))
        return types_1.EUploadMimeType.Webp;
    if (name.endsWith('.gif'))
        return types_1.EUploadMimeType.Gif;
    if (name.endsWith('.mpeg4') || name.endsWith('.mp4'))
        return types_1.EUploadMimeType.Mp4;
    if (name.endsWith('.srt'))
        return types_1.EUploadMimeType.Srt;
    (0, helpers_1.safeDeprecationWarning)({
        instance: 'TwitterApiv1ReadWrite',
        method: 'uploadMedia',
        problem: `options.mimeType is missing and filename couldn't help to resolve MIME type, so it will fallback to image/jpeg`,
        resolution: `If you except to give filenames without extensions, please specify explicitlty the MIME type using options.mimeType`,
    });
    return types_1.EUploadMimeType.Jpeg;
}
function getMimeByType(type) {
    (0, helpers_1.safeDeprecationWarning)({
        instance: 'TwitterApiv1ReadWrite',
        method: 'uploadMedia',
        problem: `you're using options.type`,
        resolution: `Remove options.type argument and migrate to options.mimeType which takes the real MIME type. ` +
            `If you're using type=longmp4, add options.longVideo alongside of mimeType=EUploadMimeType.Mp4`,
    });
    if (type === 'gif')
        return types_1.EUploadMimeType.Gif;
    if (type === 'jpg')
        return types_1.EUploadMimeType.Jpeg;
    if (type === 'png')
        return types_1.EUploadMimeType.Png;
    if (type === 'webp')
        return types_1.EUploadMimeType.Webp;
    if (type === 'srt')
        return types_1.EUploadMimeType.Srt;
    if (type === 'mp4' || type === 'longmp4')
        return types_1.EUploadMimeType.Mp4;
    return type;
}
function getMediaCategoryByMime(name, target) {
    if (name === types_1.EUploadMimeType.Mp4)
        return target === 'tweet' ? 'TweetVideo' : 'DmVideo';
    if (name === types_1.EUploadMimeType.Gif)
        return target === 'tweet' ? 'TweetGif' : 'DmGif';
    if (name === types_1.EUploadMimeType.Srt)
        return 'Subtitles';
    else
        return target === 'tweet' ? 'TweetImage' : 'DmImage';
}
exports.getMediaCategoryByMime = getMediaCategoryByMime;
function sleepSecs(seconds) {
    return new Promise(resolve => setTimeout(resolve, seconds * 1000));
}
exports.sleepSecs = sleepSecs;
async function readNextPartOf(file, chunkLength, bufferOffset = 0, buffer) {
    if (file instanceof Buffer) {
        const rt = file.slice(bufferOffset, bufferOffset + chunkLength);
        return [rt, rt.length];
    }
    if (!buffer) {
        throw new Error('Well, we will need a buffer to store file content.');
    }
    let bytesRead;
    if (typeof file === 'number') {
        bytesRead = await new Promise((resolve, reject) => {
            fs.read(file, buffer, 0, chunkLength, bufferOffset, (err, nread) => {
                if (err)
                    reject(err);
                resolve(nread);
            });
        });
    }
    else {
        const res = await file.read(buffer, 0, chunkLength, bufferOffset);
        bytesRead = res.bytesRead;
    }
    return [buffer, bytesRead];
}
exports.readNextPartOf = readNextPartOf;
