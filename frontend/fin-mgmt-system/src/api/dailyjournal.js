import request from '../utils/request';

export function fetchDailyData(dailyquery) {
    return request({
        url: '/dailyjournal/',
        method: 'get',
        params: dailyquery
    });
};