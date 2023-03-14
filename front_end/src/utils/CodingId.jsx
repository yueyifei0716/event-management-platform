// encode the orignal host or user id before passing it to the server
function encodeId(id) {
    if (typeof id === 'string') {
        id = parseInt(id)
    }
    let encoding = parseInt((id + 20) * 18 - 11)
    encoding = encoding.toString()
    encoding = encoding.split('')
    let res = ''

    for (let i = 0; i < encoding.length; i++) {
        if (encoding[i] === '9') {
            encoding[i] = '10'
        } else {
            encoding[i] = (parseInt(parseFloat(encoding[i]) + 1)).toString()
        }
    }

    for (let i = 0; i < encoding.length; i++) {
        res += encoding[i]
    }

    if (typeof res === 'string') {
        res = parseInt(res)
    }

    res += 192
    return res
}

// decode the encoded host or user id got from the server (in register or login)
function decodeId(encoded_id) {
    const encode_key = { 1:9, 2:4, 3:2, 4:7, 5:3, 6:8, 7:1, 8:6, 9:5, 0:0 }
    if (typeof encoded_id === 'string') {
        encoded_id = parseInt(encoded_id)
    }
    let decoding = parseInt((encoded_id - 29) / 2)
    decoding = decoding.toString()
    decoding = decoding.split('')
    let res = ''

    for (let i = 0; i < decoding.length; i++) {
        let j = parseInt(parseFloat(decoding[i]))
        decoding[i] = Object.keys(encode_key).find(key => encode_key[key] === j)
    }

    for (let i = 0; i < decoding.length; i++) {
        res += decoding[i]
    }

    if (typeof res === 'string') {
        res = parseInt(res)
    }

    res = (Math.sqrt(res - 9) - 11)
    console.log(res)

    return res
}

export { encodeId, decodeId }
