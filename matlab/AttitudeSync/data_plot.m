load('csa-non-damping.mat');

T = D1(:,1);
Ref = D1(:,8);
DataLen = size(T);

D1Error1 = D1(:,2) - D1(:,8);
D1Error2 = D1(:,3) - D1(:,8);
D1Error3 = D1(:,4) - D1(:,8);
D1Error4 = D1(:,5) - D1(:,8);
D1Error5 = D1(:,6) - D1(:,8);
D1Error6 = D1(:,7) - D1(:,8);

D2Error1 = D2(:,2) - D2(:,8);
D2Error2 = D2(:,3) - D2(:,8);
D2Error3 = D2(:,4) - D2(:,8);
D2Error4 = D2(:,5) - D2(:,8);
D2Error5 = D2(:,6) - D2(:,8);
D2Error6 = D2(:,7) - D2(:,8);

D3Error1 = D3(:,2) - D3(:,8);
D3Error2 = D3(:,3) - D3(:,8);
D3Error3 = D3(:,4) - D3(:,8);
D3Error4 = D3(:,5) - D3(:,8);
D3Error5 = D3(:,6) - D3(:,8);
D3Error6 = D3(:,7) - D3(:,8);

D1errorVar = [];
D1errorMean = [];
D2errorVar = [];
D2errorMean = [];
D3errorVar = [];
D3errorMean = [];

errorMean = [];
errorVar = []


for i=1:1:DataLen

    D1error_i = [D1Error1(i), D1Error2(i), D1Error3(i), D1Error4(i), D1Error5(i), D1Error6(i)];
    D2error_i = [D2Error1(i), D2Error2(i), D2Error3(i), D2Error4(i), D2Error5(i), D2Error6(i)];
    D3error_i = [D3Error1(i), D3Error2(i), D3Error3(i), D3Error4(i), D3Error5(i), D3Error6(i)];
    
    d1_e = norm(abs(D1error_i),2);
    d2_e = norm(abs(D2error_i),2);
    d3_e = norm(abs(D3error_i),2);
    d1_v = var(D1error_i);
    d2_v = var(D2error_i);
    d3_v = var(D3error_i);
    D1errorMean = [D1errorMean d1_e];
    D1errorVar = [D1errorVar d1_v];
    D2errorMean = [D2errorMean d2_e];
    D2errorVar = [D2errorVar d2_v];
    D3errorMean = [D3errorMean d3_e];
    D3errorVar = [D3errorVar d3_v];
    
    errorMean = [errorMean; sqrt((d1_e.^2 + d2_e.^2 + d3_e.^2)/3)];
    errorVar = [errorVar; sqrt((d1_v.^2 + d2_v.^2 + d3_v.^2)/3)];
end

figure;
plot(T, D1errorMean, T, D2errorMean, T, D3errorMean, T, errorMean);
title('root square mean error');
xlabel('Time');
legend('D1','D2','D3', 'AVG');

figure;
plot(T, D1errorVar, T, D2errorVar, T, D3errorVar, T, errorVar);
xlabel('Time');
title('error variance');
legend('D1','D2','D3', 'AVG');