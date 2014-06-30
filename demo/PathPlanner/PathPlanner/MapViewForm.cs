﻿using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Windows.Forms;
using PathPlanner.Data;
using PathPlanner.Hexagonal;
using PathPlanner.Planner;

namespace PathPlanner
{
    public partial class MapViewForm : Form
    {
        private PixelMap.PixelMap pixelMap;
        private MapInfoManager infoMgr;
        private string workingPath;
        private string mapFilepath;
        public ParamMgr paramMgr;
        public HexagonalMap map;
        private HexagonalMapDrawer mapDrawer;

        private int widthNum;
        private int heightNum;

        private bool mapVisible = true;

        public enum PathPlanMode {MAX_INFO, MIN_DIST, RANDOM };

        public PathPlanMode planMode;

        public Hex startHex;
        public Hex endHex;

        int currentCursorX = 0;
        int currentCursorY = 0;

        public Robot robot;

        public HexaPath currentPath;

        PathManager pathMgr;

        public MapViewForm()
        {
            infoMgr = new MapInfoManager();
            paramMgr = new ParamMgr();
            planMode = PathPlanMode.MIN_DIST;
            InitializeComponent();
            currentPath = null;
            pathMgr = null;
        }

        private void openToolStripMenuItem_Click(object sender, EventArgs e)
        {
            this.mapViewOpenFileDialog.ShowDialog();
        }

        private void mapViewOpenFileDialog_FileOk(object sender, CancelEventArgs e)
        {
            try
            {
                workingPath = System.IO.Path.GetDirectoryName(this.mapViewOpenFileDialog.FileName);
                infoMgr.LoadFile(this.mapViewOpenFileDialog.FileName);

                this.mapFilepath = System.IO.Path.Combine(workingPath, infoMgr.mapFilename);
                
                this.pixelMap = new PixelMap.PixelMap(this.mapFilepath);
                //this.mapViewPictureBox.BackgroundImage = this.pixelMap.GreyMap;
                this.mapViewPictureBox.BackgroundImage = this.pixelMap.GetTransparentMap(50);
                this.mapViewPictureBox.Size = new Size(this.pixelMap.Header.Width, this.pixelMap.Header.Height);
                this.mapViewPanel.Size = this.mapViewPictureBox.Size;
                this.mapViewPanel.AutoScroll = true;
                this.toolbarForm.Visible = true;
                this.mapToolStripMenuItem.Checked = true;

                this.saveToolStripMenuItem.Enabled = true;

                this.widthNum = (int)this.pixelMap.Header.Width / ( paramMgr.hexagonalSize);
                this.heightNum = (int)(this.pixelMap.Header.Height / (Math.Sqrt(2) * paramMgr.hexagonalSize / 2));

                this.map = new HexagonalMap(this.widthNum, this.heightNum, paramMgr.hexagonalSize, HexOrientation.Pointy);
                this.mapDrawer = new HexagonalMapDrawer(this.map);

                Random rnd = new Random();
                for (int i = 0; i < this.widthNum; i++)
                {
                    for (int j = 0; j < this.heightNum; j++)
                    {
                        //this.map.MapState.hexVals[i, j] = rnd.NextDouble();
                        this.map.MapState.hexVals[i, j] = this.infoMgr.GetDiffusionValue(i, j);           
                    }
                }

                this.map.MapState.NormalizeHexVal();
                //this.map.MapState.DumpHexValToFile("test.csv");

                for (int i = 0; i < this.widthNum; i++)
                {
                    for (int j = 0; j < this.heightNum; j++)
                    {
                        this.map.GetMapStateMgr().SetEntropy(i, j, this.map.MapState.hexVals[i,j]);
                    }
                }

                /*
                for (int i = 0; i < this.pixelMap.BitMap.Width; i++)
                {
                    for (int j = 0; j < this.pixelMap.BitMap.Height; j++)
                    {
                        Color c = this.pixelMap.BitMap.GetPixel(i, j);
                        Console.WriteLine("[" + i.ToString() + "," + j.ToString() + "]:" + c.R.ToString() + " " + c.G.ToString() + " " + c.B.ToString());
               
                    }
                }
                 */

                for (int i = 0; i < this.map.mapWidth; i++)
                {
                    for (int j = 0; j < this.map.mapHeight; j++)
                    {
                        List<System.Drawing.PointF> points = this.map.GetHex(i,j).inPointSet;
                        int obsCnt = 0;
                        List<System.Drawing.PointF>.Enumerator eP = points.GetEnumerator();
                        while (eP.MoveNext())
                        {
                            int tX = (int)System.Math.Floor(eP.Current.X);
                            int tY = (int)System.Math.Floor(eP.Current.Y);

                            int bW = this.pixelMap.BitMap.Width;
                            int bH = this.pixelMap.BitMap.Height;

                            if (tX > (bW - 1))
                            {
                                tX = bW - 1;
                            }
                            if(tY > (bH - 1))
                            {
                                tY = bH - 1;
                            }

                            Color tColor = this.pixelMap.BitMap.GetPixel(tX, tY);
                            if ((int)tColor.R < 200 || (int)tColor.G < 200 || (int)tColor.B < 200)
                            {
                                obsCnt++;
                            }
                        }

                        //if (obsCnt * 2 > points.Count)
                        if(obsCnt > 0)
                        {
                            this.map.mapState.AddObstalce(this.map.GetHex(i, j));
                        }

                    }
                }

                robot = new Robot(map);
                this.pathMgr = new PathManager(map, infoMgr.mapFilename);
                 
            }
            catch (Exception ex)
            {
                ShowException(ex);
            }
        }

        private void ShowException(Exception ex)
        {
            string message = ex.InnerException.Message;
            string caption = "PixelMap Error! " + ex.Message;
            MessageBox.Show(message, caption, MessageBoxButtons.OK, MessageBoxIcon.Error);
        }

        private void configToolStripMenuItem_Click(object sender, EventArgs e)
        {
            if (paramMgr.IsView == true)
            {
                paramMgr.ViewForm(false);
            }
            else
            {
                paramMgr.ViewForm(true);
            }
            Refresh();
        }

        private void MapViewForm_Paint(object sender, PaintEventArgs e)
        {
            if (this.paramMgr.IsView == true)
            {
                this.configToolStripMenuItem.Checked = true;
            }
            else
            {
                this.configToolStripMenuItem.Checked = false;
            }

            if (this.toolbarForm.Visible == true)
            {
                this.toobarToolStripMenuItem.Checked = true;
            }
            else
            {
                this.toobarToolStripMenuItem.Checked = false;
            }
        }

        private void mapViewPictureBox_Paint(object sender, PaintEventArgs e)
        {
            this.infoMgr.featureMgr.Draw(e.Graphics);
            this.infoMgr.indoorMgr.Draw(e.Graphics);
            this.infoMgr.outdoorMgr.Draw(e.Graphics);
        }

        private void toobarToolStripMenuItem_Click(object sender, EventArgs e)
        {
            if (this.toolbarForm.Visible == true)
            {
                this.toolbarForm.Visible = false;
            }
            else
            {
                this.toolbarForm.Visible = true;
            }
            Refresh();
        }

        private void exitToolStripMenuItem_Click(object sender, EventArgs e)
        {
            Application.Exit();
        }

        private void mapToolStripMenuItem_Click(object sender, EventArgs e)
        {
            if (this.mapViewPictureBox.Visible == true)
            {
                this.mapViewPictureBox.Visible = false;
                this.mapToolStripMenuItem.Checked = false;
            }
            else
            {
                this.mapViewPictureBox.Visible = true;
                this.mapToolStripMenuItem.Checked = true;
            }
            Refresh();
        }

        private void hexagonToolStripMenuItem_Click(object sender, EventArgs e)
        {
            if (this.mapVisible == true)
            {
                this.mapVisible = false;
                this.hexagonToolStripMenuItem.Checked = false;
            }
            else
            {
                this.mapVisible = true;
                this.hexagonToolStripMenuItem.Checked = true;
            }

            Refresh();
        }

        private void mapViewPanel_Paint(object sender, PaintEventArgs e)
        {
            if (mapVisible == true)
            {
                if (mapDrawer!=null)
                {
                    mapDrawer.Draw(e.Graphics);
                }
            }
        }

        private void mapViewPanel_MouseClick(object sender, MouseEventArgs e)
        {
            if (e.Button == MouseButtons.Right)
            {
                if (this.planMode == MapViewForm.PathPlanMode.MIN_DIST)
                {
                    // pop to choose "complete" or "cancel"
                    this.cmsAddPoint.Show(this.Left + e.X, this.Top + e.Y);
                    this.currentCursorX = e.X;
                    this.currentCursorY = e.Y;
                }
                else
                {

                    Point mouseClick = new Point(e.X - mapDrawer.BoardXOffset, e.Y - mapDrawer.BoardYOffset);
                    Hex clickedHex = map.FindHexMouseClick(mouseClick);

                    this.startHex = clickedHex;
                    map.MapState.ActiveHex = clickedHex;
                    Refresh();
                }
                
            }
        }

        private void startToolStripMenuItem_Click(object sender, EventArgs e)
        {
            Point mouseClick = new Point(currentCursorX - mapDrawer.BoardXOffset, currentCursorY - mapDrawer.BoardYOffset);
            Hex clickedHex = map.FindHexMouseClick(mouseClick);

            this.startHex = clickedHex;
            map.MapState.ActiveHex = clickedHex;

            Refresh();
        }

        private void endToolStripMenuItem_Click(object sender, EventArgs e)
        {
            Point mouseClick = new Point(currentCursorX - mapDrawer.BoardXOffset, currentCursorY - mapDrawer.BoardYOffset);
            Hex clickedHex = map.FindHexMouseClick(mouseClick);

            this.endHex = clickedHex;
            map.MapState.ActiveHex2 = clickedHex;

            Refresh();
        }

        private void saveToolStripMenuItem_Click(object sender, EventArgs e)
        {
            this.mapViewSaveFileDialog.ShowDialog();
        }

        private void mapViewSaveFileDialog_FileOk(object sender, CancelEventArgs e)
        {
            if (currentPath != null)
            {
                pathMgr.DumpPath(currentPath, this.mapViewSaveFileDialog.FileName);               
            }
        }
    }
}
