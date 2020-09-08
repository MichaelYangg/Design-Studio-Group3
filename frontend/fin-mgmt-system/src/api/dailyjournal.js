import request from '../utils/request';

export const fetchDailyData = dailyquery => {
    return request({
        url: '/daily/',
        method: 'get',
        params: dailyquery
    });
};