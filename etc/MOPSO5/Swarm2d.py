'''
Created on 2013-12-5

@author: Walter
'''

from Swarm import *;
          
class Swarm2D(Swarm):
    
    def initReferenceSet(self, loadFromFile=False, nondomSetFile=None, domSetFile=None):        
        self.referenceSet = [];
        idxCnt = 0;
        for x in np.arange(-self.worldrange[0]/2, self.worldrange[0]/2, 0.05):
            for y in np.arange(-self.worldrange[1]/2, self.worldrange[1]/2, 0.05):  
                ref = Reference(self.particleDimension, idxCnt);
                ref.pos[0,0] = x;
                ref.pos[0,1] = y;
                self.referenceSet.append(ref);
                idxCnt += 1;
            
        self.categorizeRefSet(loadFromFile, nondomSetFile, domSetFile);
        self.initDomFit();
        self.initNondomFit();
        
            
    def initDomFit(self):
        for domPos in self.dominatedSet:
            domPos.fit = [];
            domPos.fit.append(self.calcObjFunc(domPos.pos, 0));
            domPos.fit.append(self.calcObjFunc(domPos.pos, 1));
            
    def initNondomFit(self):
        for nondomPos in self.nondominatedSet:
            nondomPos.fit = [];
            nondomPos.fit.append(self.calcObjFunc(nondomPos.pos, 0));
            nondomPos.fit.append(self.calcObjFunc(nondomPos.pos, 1));
            
    def getDomFit(self):
        fit1 = [];
        fit2 = [];
        for domPos in self.dominatedSet:
            fit1.append(domPos.fit[0]);
            fit2.append(domPos.fit[1]);
        return fit1, fit2;
        
    def getNondomFit(self):
        fit1 = [];
        fit2 = [];
        for nondomPos in self.nondominatedSet:
            fit1.append(nondomPos.fit[0]);
            fit2.append(nondomPos.fit[1]);
        return fit1, fit2;
            
    def getXYDominate(self):        
        xPos = [];
        yPos = []
        for a in self.dominatedSet:
            xPos.append(a.pos[0,0]);
            yPos.append(a.pos[0,1]);
        return xPos, yPos;
        
    def getXYNondominate(self):
        xPos = [];
        yPos = []
        for a in self.nondominatedSet:
            xPos.append(a.pos[0,0]);
            yPos.append(a.pos[0,1]);
        return xPos, yPos;   
    
    def getDominatedParticlePos(self):        
        xDomParPos = [];
        yDomParPos = [];
        for p in self.dominatedParticles:
            assert p.nondominated == False;
            xDomParPos.append(p.pos[0,0]);
            yDomParPos.append(p.pos[0,1]);
        return xDomParPos, yDomParPos;
    
    def getNondominatedParticlePos(self):
        xNondomParPos = [];
        yNondomParPos = [];
        for p in self.nondominatedParticles:
            assert p.nondominated == True;
            xNondomParPos.append(p.pos[0,0]);
            yNondomParPos.append(p.pos[0,1]);
        return xNondomParPos, yNondomParPos; 
        
    def plot(self, count, path=None):
            
        fig1 = plt.figure();
        ax1 = fig1.add_subplot(111);

        
        domPosX, domPosY = self.getXYDominate();
        ax1.plot(domPosX, domPosY, 's', color = '#aaaaaa');
        nondomPosX, nondomPosY = self.getXYNondominate();
        ax1.plot(nondomPosX, nondomPosY, 's', color='#7a7a7a');
        ax1.legend(['dom', 'nondom'])
        
        '''
        posX = [];
        posY = [];
        for p in self.particles:
            posX.append(p.pos[0,0]);
            posY.append(p.pos[0,1]);

        ax1.plot(posX, posY, 'or');
        '''
        domPX, domPY = self.getDominatedParticlePos();
        nondomPX, nondomPY = self.getNondominatedParticlePos();
        ax1.plot(domPX, domPY, 'o', color='#0000ff');
        ax1.plot(nondomPX, nondomPY, 'o', color='#ff0000');
    
        
        #globalbest = self.particles[self.globalbestAgentIdx];
        #ax1.plot(globalbest.localbestPos[0,0], globalbest.localbestPos[0,1], 'ob');
        ax1.plot(self.globalbestPos[0,0], self.globalbestPos[0,1], 'o', color='yellow');
        ax1.plot(self.swarm_centroid[0,0], self.swarm_centroid[0,1], 's', color='orange');
        ax1.set_xlabel("particle x position");
        ax1.set_ylabel("particle y position");
        title1 = "2D solution space @ " + str(count);
        ax1.set_title(title1);
        filename1 = title1 + ".png";
        if path != None:
            filename1 = path + "\\" + filename1;
        plt.savefig(filename1); 
        
        fig2 = plt.figure();
        ax2 = fig2.add_subplot(111);
        
        domx_fit = [];
        domy_fit = [];
        for p in self.dominatedParticles:
            domx_line = [p.pos[0,0], p.pos[0,0] + p.vel[0,0] * self.interval];
            domy_line = [p.pos[0,1], p.pos[0,1] + p.vel[0,1] * self.interval];
            pos = [p.pos[0,0], p.pos[0,1]];
            domx_fit.append(self.objfuncs[0](pos));
            domy_fit.append(self.objfuncs[1](pos));
            ax1.plot(domx_line, domy_line, '-b');
        
        nondomx_fit = [];
        nondomy_fit = [];
        for p in self.nondominatedParticles:
            nondomx_line = [p.pos[0,0], p.pos[0,0] + p.vel[0,0] * self.interval];
            nondomy_line = [p.pos[0,1], p.pos[0,1] + p.vel[0,1] * self.interval];
            pos = [p.pos[0,0], p.pos[0,1]];
            nondomx_fit.append(self.objfuncs[0](pos));
            nondomy_fit.append(self.objfuncs[1](pos));
            ax1.plot(nondomx_line, nondomy_line, '-b');
    
        domfit1, domfit2 = self.getDomFit();
        nondomfit1, nondomfit2 = self.getNondomFit();
        
        #print str(len(self.dominatedSet)) + " " + str(len(self.nondominatedSet));
        ax2.plot(domfit1, domfit2, '.', color='#aaaaaa');
        ax2.plot(nondomfit1, nondomfit2, '.', color='#7a7a7a');
        ax2.legend(['dom', 'nondom']);
        
        '''
        x_range = [];
        y_range = [];
        for x in np.arange(-self.worldrange[0]/2, self.worldrange[0]/2, 0.05):
            for y in np.arange(-self.worldrange[1]/2, self.worldrange[1]/2, 0.05):
                pos = [x, y];
                x_range.append(self.objfuncs[0](pos));
                y_range.append(self.objfuncs[1](pos));
        ax2.plot(x_range, y_range, '.r');
        '''     
        ax2.plot(domx_fit, domy_fit, 'ob');
        ax2.plot(nondomx_fit, nondomy_fit, 'og');
        
        ax2.plot(self.swarm_centroid_fitness[0,0], self.swarm_centroid_fitness[0,1], 's', color='orange');
        ax2.plot(self.average_fitness[0,0], self.average_fitness[0,1], 'x', color='brown');
        ax2.set_xlabel("Fitness 1");
        ax2.set_ylabel("Fitness 2");
        title2 = "2D fitness space @ " + str(count);
        ax2.set_title(title2);
        filename2 = title2 + ".png";
        if path != None:
            filename2 = path + "\\" + filename2;
        plt.savefig(filename2); 
        
        if len(self.histCentroid) > 0 and self.showCentroidHist==True:
            fig3 = plt.figure();
            ax3 = fig3.add_subplot(111);
            idx3 = [];
            ctX = [];
            ctY = [];
                    
            for i in range(len(self.histCentroid)):
                idx3.append(i);
                ctX.append(self.histCentroid[i][0,0]);
                ctY.append(self.histCentroid[i][0,1]);
                
            ax3.plot(idx3, ctX);
            ax3.plot(idx3, ctY);
            ax3.set_xlabel("Iteration");
            ax3.set_ylabel("Position");
            ax3.legend(["Position X","Position Y"]);
            title3 = "2D Centroid of " + str(count) + " run";
            ax3.set_title(title3);
            filename3 = title3 + ".png";
            if path != None:
                filename3 = path + "\\" + filename3;
            plt.savefig(filename3); 
            
        if len(self.histAvgFitness) > 0 and self.showAverageFitness==True:    
            fig4 = plt.figure();
            ax4 = fig4.add_subplot(111);      
            idx4 = []
            avX = [];
            avY = [];

            for i in range(len(self.histAvgFitness)):
                idx4.append(i);
                avX.append(self.histAvgFitness[i][0,0]);
                avY.append(self.histAvgFitness[i][0,1]);   

            ax4.plot(idx4, avX);
            ax4.plot(idx4, avY);
            ax4.set_xlabel("Iteration");
            ax4.set_ylabel("Value");
            ax4.legend(["Function 1","Function 2"]);
            title4 = "2D Average Fitness of " + str(count) + " run";
            ax4.set_title(title4);
            filename4 = title4 + ".png";
            if path != None:
                filename4 = path + "\\" + filename4;
            plt.savefig(filename4); 
            
        if len(self.histCentroidMaximin) > 0 and self.showMaximinOfCentroid==True:    
            fig5 = plt.figure();
            ax5 = fig5.add_subplot(111);      
            idx5 = np.arange(len(self.histCentroidMaximin));

            ax5.plot(idx4, self.histCentroidMaximin);
            ax5.set_xlabel("Iteration");
            ax5.set_ylabel("Value");
            title5 = "2D Maximin Value of Centroid in " + str(count) + " run";
            ax5.set_title(title5);
            filename5 = title5 + ".png";
            if path != None:
                filename5 = path + "\\" + filename5;
            plt.savefig(filename5);  
        
        if len(self.histGlobalbestPos) > 0 and self.showGlobalBestPosition==True:
            fig6 = plt.figure();
            ax6 = fig6.add_subplot(111);
            idx6 = [];
            gbX = [];
            gbY = [];
                    
            for i in range(len(self.histCentroid)):
                idx6.append(i);
                gbX.append(self.histGlobalbestPos[i][0]);
                gbY.append(self.histGlobalbestPos[i][1]);
                
            ax6.plot(idx6, gbX);
            ax6.plot(idx6, gbY);
            ax6.set_xlabel("Iteration");
            ax6.set_ylabel("Position");
            ax6.legend(["Position X", "Position Y"]);
            title6 = "2D Global Best Position of " + str(count) + " run";
            ax6.set_title(title6);
            filename6 = title6 + ".png";
            if path != None:
                filename6 = path + "\\" + filename6;
            plt.savefig(filename6);   
            
        if len(self.histPercentOfNondominance) > 0 and self.showPercentOfNondominance == True:
            fig7 = plt.figure();
            ax7 = fig7.add_subplot(111);
            idx7 = np.arange(len(self.histPercentOfNondominance));
            ax7.plot(idx7, self.histPercentOfNondominance);
            ax7.set_xlabel("Iteration");
            ax7.set_ylabel("Percentage");
            ax7.legend(["Percentage"]);
            title7 = "2D Percentage of nondominance " + str(count) + " run";
            ax7.set_title(title7);
            filename7 = title7 + ".png";
            if path != None:
                filename7 = path + "\\" + filename7;
            plt.savefig(filename7); 
            
        if len(self.histPosVariance) > 0 and self.showPosVariance == True:
            fig8 = plt.figure();
            ax8 = fig8.add_subplot(111);
            idx8 = np.arange(len(self.histPosVariance));
            for d in range(self.particleDimension):
                variance = [];
                paretoVar = [];
                for idx in range(len(self.histPosVariance)):
                    variance.append(self.histPosVariance[idx][d]);
                    paretoVar.append(self.paretoVar[d]);
                ax8.plot(idx8, paretoVar);
                ax8.plot(idx8, variance);
            ax8.set_xlabel("Iteration");
            ax8.set_ylabel("Variance");
            ax8.legend(["Pareto Variance x", "Variance x", "Pareto Variance y", "Variance y"]);
            title8 = "2D Pos Variance " + str(count) + " run";
            ax8.set_title(title8);
            filename8 = title8 + ".png";
            if path != None:
                filename8 = path + "\\" + filename8;
            plt.savefig(filename8); 
        
        if len(self.histFitVariance) > 0 and self.showFitVariance == True:
            fig9 = plt.figure();
            ax9 = fig9.add_subplot(111);
            idx9 = np.arange(len(self.histFitVariance));
            ax9.plot(idx9, self.histFitVariance);
            ax9.set_xlabel("Iteration");
            ax9.set_ylabel("Variance");
            ax9.legend(["Variance"]);
            title9 = "2D Fit Variance " + str(count) + " run";
            ax9.set_title(title9);
            filename9 = title9 + ".png";
            if path != None:
                filename9 = path + "\\" + filename9;
            plt.savefig(filename9);                      
        
        if len(self.histHausdorffDist)  > 0 and self.showHausdorffDist == True:
            fig10 = plt.figure();
            ax10 = fig10.add_subplot(111);
            idx10 = np.arange(len(self.histHausdorffDist));
            ax10.plot(idx10, self.histHausdorffDist);
            ax10.set_xlabel("Iteration");
            ax10.set_ylabel("Distance");
            title10 = "2D Hausdorff Distance " + str(count) + "run";
            ax10.set_title(title10);
            filename10 = title10 + ".png";
            if path != None:
                filename10 = path + "\\" + filename10;
            plt.savefig(filename10);   
        
        if self.gbSet.kernel != None:
            fig11 = plt.figure();
            ax11 = fig11.add_subplot(111);
            X = self.gbSet.kernel.resample(1000);
            #ax11.plot(X[0], X[1], '.')
            ax11.hist(X[0], 30, normed=1, histtype='stepfilled');
            ax11.hist(X[1], 30, normed=1, histtype='stepfilled');
            title11 = "2D " + str(len(self.gbSet.nondomObs)) +  " global estimated distribution " + str(count) + "run";
            ax11.set_title(title11);
            filename11 = title11 + ".png";
            if path != None:
                filename11 = path + "\\" + filename11;
            plt.savefig(filename11);
        
            
        #plt.show();