import request from '../utils/request';

export function fetchData(query) {
    return request({
        url: '/transactions/',
        method: 'GET',
        params: query
    });
};