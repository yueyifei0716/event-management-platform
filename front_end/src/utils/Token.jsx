import { encodeId } from "./CodingId";


// extract the user id from the localStorage
function extractUserId(token) {
    let user_id = localStorage.getItem("user_id");
    if (user_id === '' || user_id === null) {
        return null;
    }
    return encodeId(user_id);
}

// extract the host id from the localStorage
function extractHostId(token) {
    let host_id = localStorage.getItem("host_id");
    if (host_id === '' || host_id === null) {
        return null;
    }
    return encodeId(host_id);
}

export { extractUserId, extractHostId }
