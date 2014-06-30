﻿using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Windows.Forms;
using PathPlanner;
using PathPlanner.Hexagonal;
using PathPlanner.Planner;

namespace PathPlanner
{
    public partial class ToolbarForm : Form
    {
        MapViewForm mapViewForm;

        public ToolbarForm(MapViewForm form)
        {
            mapViewForm = form;
            InitializeComponent();
            switch(this.mapViewForm.planMode)
            {
                case MapViewForm.PathPlanMode.MAX_INFO:
                default:
                    this.rbInfoMax.Checked = true;
                    break;
                case MapViewForm.PathPlanMode.MIN_DIST:
                    this.rbDistMin.Checked = true;
                    break;
                case MapViewForm.PathPlanMode.RANDOM:
                    this.rbRandom.Checked = true;
                    break;
            }

        }

        private void tbPlan_Click(object sender, EventArgs e)
        {
            int planLength = 0;
            if (this.tbPlanLength.Text != "")
            {
                planLength = Int32.Parse(this.tbPlanLength.Text);
            }
            else
            {
                planLength = 0;
            }

            Random rnd = new Random();
            int start_x = this.mapViewForm.map.mapState.ActiveHex.posX;
            int start_y = this.mapViewForm.map.mapState.ActiveHex.posY;
            HexaPos pos = new HexaPos(start_x, start_y);

            if (this.rbRandom.Checked == true)
            {
                HexaPath path = new HexaPath();
                path.AddPos(pos);
                for (int t = 0; t < planLength; t++)
                {
                    int rndIdx = rnd.Next(5);
                    HexagonalMap.Direction direction = mapViewForm.map.directionList[rndIdx];
                    HexaPos newPos = mapViewForm.map.GetNext(path[t], direction);
                    path.AddPos(newPos);

                }

                LoadActivePath(path);

                mapViewForm.Refresh();
            }
            else if(this.rbInfoMax.Checked == true)
            {
                InfoMaxPathPlanner planner
                    = new InfoMaxPathPlanner(mapViewForm.map, (Robot)mapViewForm.robot);

                HexaPos startPos = new HexaPos(mapViewForm.startHex.posX, mapViewForm.startHex.posY);

                TopologyGraphGenerator topologyGenerator = new TopologyGraphGenerator(mapViewForm.map);
                TopologyGraph tograph = topologyGenerator.GetTopologyGraph();
                tograph.Draw();
                PlanningGraphGenerator planningGenerator = new PlanningGraphGenerator(tograph);
                PathPlanningGraph graph = planningGenerator.GetPathPlanningGraph(startPos, Int32.Parse(this.tbPlanLength.Text));
                graph.Draw();
                planner.iteratingOnce = true;
                HexaPath maxPath = planner.FindPath(graph, startPos);

                LoadActivePath(maxPath);

                mapViewForm.Refresh();
            }
            else if (this.rbDistMin.Checked == true)
            {
                DistMinPathPlanner planner = new DistMinPathPlanner(mapViewForm.map, (Robot)mapViewForm.robot);
                HexaPos startPos = new HexaPos(mapViewForm.startHex.posX, mapViewForm.startHex.posY);
                HexaPos endPos = new HexaPos(mapViewForm.endHex.posX, mapViewForm.endHex.posY);

                TopologyGraphGenerator topologyGenerator = new TopologyGraphGenerator(mapViewForm.map);
                TopologyGraph tograph = topologyGenerator.GetTopologyGraph();

                HexaPath path = planner.FindPath(tograph, startPos, endPos);

                LoadActivePath(path);
                mapViewForm.Refresh();
            }
        }

        private void LoadActivePath(HexaPath path)
        {
            mapViewForm.map.mapState.ActiveHexSet = new HexSet(mapViewForm.map.mapState);
            for (int t = 1; t < path.Length; t++)
            {
                Hex hex = mapViewForm.map.GetHex(path[t].X, path[t].Y);
                mapViewForm.map.mapState.ActiveHexSet.hexSet.Add(hex);
            }
            mapViewForm.currentPath = path;
        }

        private void rbDistMin_Click(object sender, EventArgs e)
        {
            if (this.rbDistMin.Checked == true)
            {
                this.mapViewForm.planMode = MapViewForm.PathPlanMode.MIN_DIST;
            }
        }

        private void rbInfoMax_Click(object sender, EventArgs e)
        {
            if (this.rbInfoMax.Checked == true)
            {
                this.mapViewForm.planMode = MapViewForm.PathPlanMode.MAX_INFO;
            }
        }

        private void rbRandom_Click(object sender, EventArgs e)
        {
            if (this.rbRandom.Checked == true)
            {
                this.mapViewForm.planMode = MapViewForm.PathPlanMode.RANDOM;
            }
        }



    }
}
