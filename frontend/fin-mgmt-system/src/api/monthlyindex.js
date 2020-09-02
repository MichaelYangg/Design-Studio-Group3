import request from '../utils/request';

export const fetchMonthlyData = monthlyquery => {
    return request({
        url: './monthlyjournal.json',
        method: 'get',
        params: monthlyquery
    });
};