import request from '../utils/request';

export const fetchDailyData = dailyquery => {
    return request({
        url: './dailyjournal.json',
        method: 'get',
        params: dailyquery
    });
};