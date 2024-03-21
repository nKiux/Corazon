using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Threading;
using System.Threading.Tasks;
using System.Windows.Forms;

namespace WindowsFormsApp1
{
    public partial class Form1 : Form
    {
        public Form1()
        {
            InitializeComponent();
        }

        private void Form1_Load(object sender, EventArgs e)
        {

        }

        private void label1_Click(object sender, EventArgs e)
        {
            label1.Text = "TEST1";
            label1.Refresh();
        }

        private void button1_Click(object sender, EventArgs e)
        {
            progressBar1.Value = 0;
            label1.Text = "ACTION1";
            label1.Refresh();
            for(int i = 0; i < 10; i++)
            {
                progressBar1.Value += 10;
                System.Threading.Thread.Sleep(1);
            }
        }

        private void progressBar1_Click(object sender, EventArgs e)
        {

        }

        private void button2_Click(object sender, EventArgs e)
        {
            System.Windows.Forms.Application.Exit();
        }
    }
}
