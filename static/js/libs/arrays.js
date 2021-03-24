/**
 * Checks the items in an array are equal.
 * The order of the items doesn't matter
 *
 * @param {array} oldArray
 * @param {array} newArray
 * @returns {boolean}
 */
function arraysEqual(oldArray, newArray) {
  if (oldArray === newArray) {
    return true;
  }
  if (
    oldArray === null ||
    newArray === null ||
    oldArray.length !== newArray.length
  ) {
    return false;
  }

  const _oldArray = [...oldArray];
  const _newArray = [...newArray];

  _oldArray.sort();
  _newArray.sort();

  for (let i = 0; i < _oldArray.length; i++) {
    if (JSON.stringify(_oldArray[i]) !== JSON.stringify(_newArray[i])) {
      return false;
    }
  }

  return true;
}

/**
 * Splits an array into chunks
 * @param {array} arr
 * @param {number} chunkSize
 * @returns {array}
 */
function arrayChunk(arr, chunkSize) {
  const chunks = [];
  const arrCopy = arr.slice(0);

  for (let i = 0, ii = arrCopy.length; i < ii; i += chunkSize) {
    chunks.push(arrCopy.splice(0, chunkSize));
  }

  return chunks;
}

/**
 * Merges 2 arrays and dedupes
 * @param {array} arr1
 * @param {array} arr2
 * @returns {array}
 */
function arraysMerge(arr1, arr2) {
  const arr3 = [...arr1, ...arr2];

  return arr3.filter((item, i) => arr3.indexOf(item) === i);
}

export { arraysEqual, arrayChunk, arraysMerge };
