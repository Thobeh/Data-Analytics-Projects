#!/usr/bin/env python
# coding: utf-8

# In[1]:


#!/usr/bin/env python
# coding: utf-8

# In[1]:


# coding: utf-8
import pathlib
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import customtkinter as ctk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
import pandas as pd
import seaborn as sns

# ML Imports
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.metrics import accuracy_score, mean_squared_error, r2_score

# Set modern UI theme
ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

# =========================
# Core ETL Logic
# =========================

class ETLPipeline:
    def __init__(self):
        self.df = None
        self.file_path = None

    def extract(self, file_path):
        self.file_path = pathlib.Path(file_path)
        if self.file_path.suffix == '.csv':
            self.df = pd.read_csv(self.file_path)
        else:
            self.df = pd.read_excel(self.file_path)
        return self.df

    def review_integrity(self):
        """Analyzes dataset health: missing values, duplicates, dtypes, and uniqueness."""
        if self.df is None:
            raise ValueError("No dataset loaded for integrity review.")

        # ✅ FIXED: Multi-layered fallback conditions protect the integer calculation step
        shape_tuple = self.df.shape if hasattr(self.df, 'shape') else None

        total_rows = int(shape_tuple[0]) if (shape_tuple and len(shape_tuple) > 0 and shape_tuple[0] is not None) else 0
        total_cols = int(shape_tuple[1]) if (shape_tuple and len(shape_tuple) > 1 and shape_tuple[1] is not None) else 0

        duplicate_count = int(self.df.duplicated().sum()) if hasattr(self.df, 'duplicated') else 0
        total_cells = int(total_rows * total_cols) # This math operation is now completely secure
        total_nulls = int(self.df.isnull().sum().sum()) if hasattr(self.df, 'isnull') else 0

        # Vectorized grid checking avoids type parsing loops completely
        placeholders = ['?', 'NA', 'na', 'n/a', 'N/A', '-', 'None', 'none', 'NULL', 'null']
        placeholder_count = int(self.df.isin(placeholders).sum().sum()) if hasattr(self.df, 'isin') else 0

        col_stats = []
        if hasattr(self.df, 'columns'):
            for col in self.df.columns:
                null_cnt = int(self.df[col].isnull().sum())

                if total_rows > 0:
                    null_pct = (float(null_cnt) / float(total_rows)) * 100.0
                else:
                    null_pct = 0.0

                col_stats.append({
                    "column": col,
                    "dtype": str(self.df[col].dtype),
                    "null_count": null_cnt,
                    "null_pct": f"{null_pct:.1f}%",
                    "unique_count": int(self.df[col].nunique(dropna=True)) if hasattr(self.df[col], 'nunique') else 0
                })

        # Safely process percentages with explicit protective string backups
        if total_rows > 0:
            dup_pct_str = f"{((float(duplicate_count) / float(total_rows)) * 100.0):.1f}%"
        else:
            dup_pct_str = "0%"

        if total_cells > 0:
            null_pct_str = f"{((float(total_nulls) / float(total_cells)) * 100.0):.1f}%"
        else:
            null_pct_str = "0%"

        return {
            "total_rows": total_rows,
            "total_cols": total_cols,
            "duplicate_count": duplicate_count,
            "duplicate_pct": dup_pct_str,
            "total_nulls": total_nulls,
            "null_pct": null_pct_str,
            "placeholder_count": placeholder_count,
            "col_stats": col_stats
        }


    def transform(self, placeholders=True, drop_duplicates=True, drop_nulls=False, fill_nulls=False, case_choice="none"):
        if self.df is None:
            raise ValueError("No dataset loaded for transformation.")

        initial_rows = len(self.df)
        report_lines = ["Transformation Stage Summary:\n"]

        if placeholders:
            ph = ['?', 'NA', 'na', 'n/a', 'N/A', '-', 'None', 'none', 'NULL', 'null']
            self.df.replace(ph, np.nan, inplace=True)
            report_lines.append("• Placeholders swapped with True NaN values.")

        total_nulls = self.df.isnull().sum().sum()
        report_lines.append(f"• Total missing/null cell instances tracked: {total_nulls}")

        if drop_nulls:
            self.df.dropna(inplace=True)
            null_dropped_rows = initial_rows - len(self.df)
            report_lines.append(f"• Rows dropped due to missing fields: {null_dropped_rows}")

        if drop_duplicates:
            pre_dup_count = len(self.df)
            self.df.drop_duplicates(inplace=True)
            removed_dups = pre_dup_count - len(self.df)
            report_lines.append(f"• Duplicate rows purged: {removed_dups}")

        if fill_nulls:
            fill_log = []
            for c in self.df.columns:
                if self.df[c].isnull().any():  # Only process columns that need filling
                    if pd.api.types.is_numeric_dtype(self.df[c]):
                        avg = self.df[c].mean()

                        # SAFE FALLBACK CHECK (Now correctly indented inside the loop)
                        if pd.isna(avg) or avg is None:
                            avg_value = 0.0
                            strategy_string = "Mean (Fallback Default)"
                        else:
                            avg_value = avg
                            strategy_string = f"Mean: {avg_value:.2f}"

                        self.df[c].fillna(avg_value, inplace=True)
                        fill_log.append(f"{c} ({strategy_string})")

                    else:
                        mode_series = self.df[c].mode()
                        if not mode_series.empty:
                            mod = mode_series.iloc[0]
                            self.df[c].fillna(mod, inplace=True)
                            fill_log.append(f"{c} (Mode: '{mod}')")
                        else:
                            # Fallback if a column is entirely empty strings or NaNs
                            self.df[c].fillna("N/A", inplace=True)
                            fill_log.append(f"{c} (Fallback: 'N/A')")

            summary_str = ", ".join(fill_log) if fill_log else "None (Dataset clean)"
            report_lines.append(f"• Imputation applied: {summary_str}")

        if case_choice == "lower":
            self.df.columns = [str(col).lower() for col in self.df.columns]
            report_lines.append("• Standardised column headers to lowercase.")
        elif case_choice == "upper":
            self.df.columns = [str(col).upper() for col in self.df.columns]
            report_lines.append("• Standardised column headers to UPPERCASE.")

        final_rows = len(self.df)
        report_lines.append(f"\nActive Dataset Rows Remaining: {final_rows}")
        return "\n".join(report_lines)


    def preview(self, n=100):
        if self.df is None:
            raise ValueError("No dataset loaded for preview.")
        return self.df.head(n)

    def export(self, save_path):
        if self.df is None:
            raise ValueError("No dataset loaded for export.")
        if save_path.endswith(".csv"):
            self.df.to_csv(save_path, index=False)
        elif save_path.endswith(".xlsx"):
            self.df.to_excel(save_path, index=False)
        else:
            raise ValueError("Unsupported export format.")

    def run_baseline_ml(self, target_column, feature_columns):
        if self.df is None:
            raise ValueError("No dataset loaded for model training.")

        ml_df = self.df[[target_column] + feature_columns].dropna().copy()

        if ml_df.empty:
            raise ValueError("The selected feature/target combination resulted in an empty dataset after dropping null values.")

        for col in ml_df.columns:
            if ml_df[col].dtype == 'object' or str(ml_df[col].dtype) == 'category':
                ml_df[col] = ml_df[col].astype('category').cat.codes

        X = ml_df[feature_columns]
        y = ml_df[target_column]

        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        is_classification = y.nunique() <= 10 or str(y.dtype) in ['object', 'bool', 'category']

        if is_classification:
            model = RandomForestClassifier(random_state=42)
            model.fit(X_train, y_train)
            preds = model.predict(X_test)
            acc = accuracy_score(y_test, preds)

            report = (
                f"🎯 Task Type: Classification (Random Forest)\n"
                f"📈 Baseline Testing Accuracy: {acc:.2%}\n\n"
                f"Feature Importance Split:\n"
            )
        else:
            model = RandomForestRegressor(random_state=42)
            model.fit(X_train, y_train)
            preds = model.predict(X_test)
            rmse = np.sqrt(mean_squared_error(y_test, preds))
            r2 = r2_score(y_test, preds)

            report = (
                f"🎯 Task Type: Regression (Random Forest)\n"
                f"📉 Root Mean Squared Error (RMSE): {rmse:.4f}\n"
                f"📊 R² Variance Score: {r2:.4f}\n\n"
                f"Feature Importance Split:\n"
            )

        importances = model.feature_importances_
        for col, imp in sorted(zip(feature_columns, importances), key=lambda x: x[1], reverse=True):
            report += f" • {col}: {imp:.2%}\n"

        return report

# =========================
# UI Frames & Tab Logic
# =========================

class MLTabFrame(ctk.CTkFrame):
    def __init__(self, master, pipeline_reference, status_label_reference, **kwargs):
        super().__init__(master, **kwargs)

        self.pipeline = pipeline_reference
        self.status_label = status_label_reference

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=2)
        self.grid_rowconfigure(0, weight=1)

        self.feature_checkboxes = {}

        self.setup_controls_panel()
        self.setup_output_panel()

    def setup_controls_panel(self):
        self.left_panel = ctk.CTkFrame(self)
        self.left_panel.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

        ctk.CTkLabel(self.left_panel, text="1. Select Dependent Target (Y):", font=("Arial", 12, "bold")).pack(anchor="w", padx=15, pady=(15, 5))
        self.combo_target = ctk.CTkComboBox(self.left_panel, values=["Load a dataset first..."])
        self.combo_target.pack(fill="x", padx=15, pady=5)

        ctk.CTkLabel(self.left_panel, text="2. Select Predictor Features (X):", font=("Arial", 12, "bold")).pack(anchor="w", padx=15, pady=(15, 5))
        self.scroll_features = ctk.CTkScrollableFrame(self.left_panel, height=220, label_text="Available Columns")
        self.scroll_features.pack(fill="both", expand=True, padx=15, pady=5)

        self.btn_train = ctk.CTkButton(
            self.left_panel,
            text="Run Baseline ML Architecture",
            command=self.run_ml_training,
            fg_color="green",
            hover_color="darkgreen"
        )
        self.btn_train.pack(fill="x", padx=15, pady=20)

    def setup_output_panel(self):
        self.right_panel = ctk.CTkFrame(self)
        self.right_panel.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)
        self.right_panel.grid_columnconfigure(0, weight=1)
        self.right_panel.grid_rowconfigure(1, weight=1)

        ctk.CTkLabel(self.right_panel, text="Model Performance Metrics & Logging", font=("Arial", 13, "bold")).grid(row=0, column=0, sticky="w", padx=15, pady=10)

        self.txt_ml_report = ctk.CTkTextbox(self.right_panel, font=("Consolas", 12))
        self.txt_ml_report.grid(row=1, column=0, sticky="nsew", padx=15, pady=15)
        self.txt_ml_report.insert("1.0", "System idle: Configure parameters and execute model training steps.")
        self.txt_ml_report.configure(state="disabled")

    def populate_column_selectors(self):
        if self.pipeline.df is None:
            return

        columns = list(self.pipeline.df.columns)

        self.combo_target.configure(values=columns)
        self.combo_target.set(columns[-1])

        for widget in self.scroll_features.winfo_children():
            widget.destroy()
        self.feature_checkboxes.clear()

        for col in columns:
            var = tk.BooleanVar(value=True)
            chk = ctk.CTkCheckBox(self.scroll_features, text=col, variable=var)
            chk.pack(anchor="w", padx=10, pady=4)
            self.feature_checkboxes[col] = var

    def run_ml_training(self):
        if self.pipeline.df is None:
            messagebox.showwarning("Pipeline Warning", "Ingest an active dataset tracking array first before building predictive models.")
            return

        selected_target = self.combo_target.get()
        selected_features = [col for col, var in self.feature_checkboxes.items() if var.get() and col != selected_target]

        if not selected_features:
            messagebox.showerror("Selection Error", "You must check at least one feature column (X) that is different from the target column.")
            return

        try:
            self.status_label.configure(text="Status: Compiling mathematical training arrays...", text_color="orange")
            self.txt_ml_report.configure(state="normal")
            self.txt_ml_report.delete("1.0", tk.END)
            self.txt_ml_report.insert(tk.END, "Training baseline model architecture... Please wait.\n")
            self.master.update_idletasks()

            report_output = self.pipeline.run_baseline_ml(selected_target, selected_features)

            self.txt_ml_report.delete("1.0", tk.END)
            self.txt_ml_report.insert(tk.END, report_output)
            self.txt_ml_report.configure(state="disabled")
            self.status_label.configure(text="Status: Model evaluation matrix generation complete.", text_color="green")

        except Exception as e:
            self.status_label.configure(text="Status: Machine Learning process error.", text_color="red")
            self.txt_ml_report.configure(state="disabled")
            messagebox.showerror("Pipeline Execution Failure", f"An anomaly crashed model training metrics calculations:\n{str(e)}")

# =========================
# Graphical User Interface
# =========================


class ETLDashboardApp(ctk.CTk):
    def __init__(self, on_success=None):
        super().__init__()  # Initializes the root Tkinter application
        self.pipeline = ETLPipeline()
        self.title("Data ETL & Integrity Dashboard")
        self.geometry("1200x750")

        self.on_success = on_success

        # ✅ FIX: Initialize default fallback log variable so render_summary_view never crashes on a missing attribute lookup
        # Update this line inside your ETLDashboardApp.__init__ constructor:
        self.last_imputation_log = "No active transformations executed yet on current workspace session data sheet assets."


        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.create_top_panel()
        self.create_main_tabs()
        #self.create_status_bar()


        self.status_bar = ctk.CTkFrame(self, height=30, corner_radius=0)
        self.status_bar.grid(row=2, column=0, sticky="ew", padx=10, pady=(0, 10))
        self.status_bar.grid_propagate(False)

        self.status_label = ctk.CTkLabel(
            self.status_bar,
            text="Status: System ready. No data extracted.",
            text_color="red",
            font=("Helvetica", 11, "italic"),
        )
        self.status_label.pack(side="left", padx=15, pady=2)

        self.create_main_tabs()

    def update_application_workflow_state(self):
        if self.pipeline.df is not None:
            text_status = "Status: Dataset parsed. Processing unlocked."
            status_color = "green"
        else:
            text_status = "Status: Awaiting file extraction."
            status_color = "red"

        if hasattr(self, "status_label"):
            self.status_label.configure(text=text_status, text_color=status_color)

    def create_top_panel(self):
        self.top_panel = ctk.CTkFrame(self, height=60, corner_radius=0)
        self.top_panel.grid(row=0, column=0, sticky="ew", padx=10, pady=10)
        self.top_panel.grid_propagate(False)

        self.btn_browse = ctk.CTkButton(self.top_panel, text="Load Dataset", command=self.load_file)
        self.btn_browse.grid(row=0, column=0, padx=10, pady=15, sticky="w")

        self.lbl_file_path = ctk.CTkLabel(self.top_panel, text="No file loaded.", text_color="gray")
        self.lbl_file_path.grid(row=0, column=1, padx=20, pady=15, sticky="w")

    def create_main_tabs(self):
        self.tab_view = ctk.CTkTabview(self)
        self.tab_view.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)

        self.tab_summary = self.tab_view.add("Summary Metrics")
        self.tab_columns = self.tab_view.add("Column Health")
        self.tab_transform = self.tab_view.add("Transformations")
        self.tab_preview = self.tab_view.add("Data Preview")
        self.tab_ml = self.tab_view.add("Machine Learning")

        for tab in [self.tab_summary, self.tab_columns, self.tab_transform, self.tab_preview, self.tab_ml]:
            tab.grid_columnconfigure(0, weight=1)
            tab.grid_rowconfigure(0, weight=1)

        self.setup_summary_tab()
        self.setup_columns_tab()
        self.setup_transform_tab()
        self.setup_preview_tab()

        self.ml_tab_view = MLTabFrame(self.tab_ml, self.pipeline, self)
        self.ml_tab_view.grid(row=0, column=0, sticky="nsew")

    def load_file(self):
        file_path = filedialog.askopenfilename(
            filetypes=[("Data Files", "*.csv *.xlsx *.xls"), ("CSV Files", "*.csv"), ("Excel Files", "*.xlsx *.xls")]
        )
        if not file_path:
            return

        try:
            self.lbl_file_path.configure(text="Ingesting data asset sheets...", text_color="orange")
            self.update_idletasks()

            self.pipeline.extract(file_path)
            self.lbl_file_path.configure(text=pathlib.Path(file_path).name, text_color="green")

            self.update_dashboard()
            self.ml_tab_view.populate_column_selectors()
            self.update_application_workflow_state()
            self.tab_view.set("Summary Metrics")

            # FIXED: Safely verify both reference scopes before execution to prevent NoneType math propagation
            if hasattr(self, "survey_app") and self.survey_app is not None:
                if hasattr(self.survey_app, "update_application_workflow_state"):
                    self.survey_app.update_application_workflow_state()
            elif hasattr(self, "app") and self.app is not None:
                if hasattr(self.app, "update_application_workflow_state"):
                    self.app.update_application_workflow_state()
        except Exception as e:
            self.lbl_file_path.configure(text="Ingestion failure.", text_color="red")
            self.update_application_workflow_state()
            messagebox.showerror("Pipeline Extraction Error", f"Could not process chosen spreadsheet:\n{str(e)}")

    def setup_summary_tab(self):
        # Add explicit padding inside the scrollable container layout
        self.summary_frame = ctk.CTkScrollableFrame(self.tab_summary)
        self.summary_frame.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)

        # ✅ FIXED: Enforce 5-column expansion rules on the base container frame instead of 4
        for col_idx in range(5):
            self.summary_frame.grid_columnconfigure(col_idx, weight=1, uniform="kpi_cols")

        self.lbl_no_data_sum = ctk.CTkLabel(self.summary_frame, text="Load data to populate metrics visualisations.")
        self.lbl_no_data_sum.grid(row=0, column=0, columnspan=5, pady=50) # Expanded columns span

    def setup_columns_tab(self):
        self.columns_frame = ctk.CTkFrame(self.tab_columns)
        self.columns_frame.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        self.columns_frame.grid_columnconfigure(0, weight=1)
        self.columns_frame.grid_rowconfigure(0, weight=1)

        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Treeview", background="#2a2d2e", foreground="white", fieldbackground="#2a2d2e", rowheight=25)
        style.map("Treeview", background=[('selected', '#1f538d')])

        cols = ("Column Name", "Data Type", "Null Count", "Null Percentage", "Unique Values")
        self.tree_cols = ttk.Treeview(self.columns_frame, columns=cols, show="headings")
        for col in cols:
            self.tree_cols.heading(col, text=col)
            self.tree_cols.column(col, anchor="center", width=150)

        self.tree_cols.grid(row=0, column=0, sticky="nsew")

        scrollbar = ttk.Scrollbar(self.columns_frame, orient="vertical", command=self.tree_cols.yview)
        self.tree_cols.configure(yscrollcommand=scrollbar.set)
        scrollbar.grid(row=0, column=1, sticky="ns")

    def setup_transform_tab(self):
        self.trans_frame = ctk.CTkFrame(self.tab_transform)
        self.trans_frame.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        self.trans_frame.grid_columnconfigure(0, weight=1)
        self.trans_frame.grid_columnconfigure(1, weight=2)
        self.trans_frame.grid_rowconfigure(0, weight=1)

        opts_frame = ctk.CTkFrame(self.trans_frame, width=320)
        opts_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        opts_frame.grid_propagate(False)

        self.chk_placeholders = ctk.CTkCheckBox(opts_frame, text="Replace String Placeholders (NA/null/-)")
        self.chk_placeholders.pack(anchor="w", padx=15, pady=15)
        self.chk_placeholders.select()

        self.chk_duplicates = ctk.CTkCheckBox(opts_frame, text="Purge Duplicate Records")
        self.chk_duplicates.pack(anchor="w", padx=15, pady=15)
        self.chk_duplicates.select()

        self.chk_nulls = ctk.CTkCheckBox(opts_frame, text="Drop Rows Containing Missing Fields")
        self.chk_nulls.pack(anchor="w", padx=15, pady=15)

        self.chk_fill_nulls = ctk.CTkCheckBox(opts_frame, text = "Fill nulls ( Average for numeric columns and Mode for non-numeric columns)")
        self.chk_fill_nulls.pack(anchor="w", padx=15, pady = 15)

        ctk.CTkLabel(opts_frame, text="Header Letter Casing Conversion:", font=("Arial", 12, "bold")).pack(anchor="w", padx=15, pady=10)
        self.case_var = ctk.StringVar(value="none")
        ctk.CTkRadioButton(opts_frame, text="Keep Original", variable=self.case_var, value="none").pack(anchor="w", padx=25, pady=5)
        ctk.CTkRadioButton(opts_frame, text="lowercase", variable=self.case_var, value="lower").pack(anchor="w", padx=25, pady=5)
        ctk.CTkRadioButton(opts_frame, text="UPPERCASE", variable=self.case_var, value="upper").pack(anchor="w", padx=25, pady=5)

        self.btn_run_trans = ctk.CTkButton(opts_frame, text="Run Transformations", command=self.run_transformations, fg_color="green", hover_color="darkgreen")
        self.btn_run_trans.pack(fill="x", padx=15, pady=30)

        self.btn_export = ctk.CTkButton(opts_frame, text="Export Refined File", command=self.export_file, state="disabled")
        self.btn_export.pack(fill="x", padx=15, pady=5)

        report_container = ctk.CTkFrame(self.trans_frame)
        report_container.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)
        report_container.grid_columnconfigure(0, weight=1)
        report_container.grid_rowconfigure(1, weight=1)

        ctk.CTkLabel(report_container, text="Execution System Logging", font=("Arial", 14, "bold")).grid(row=0, column=0, sticky="w", padx=15, pady=10)

        self.txt_report = ctk.CTkTextbox(report_container, font=("Consolas", 12))
        self.txt_report.grid(row=1, column=0, sticky="nsew", padx=15, pady=15)

    def setup_preview_tab(self):
        self.preview_frame = ctk.CTkFrame(self.tab_preview)
        self.preview_frame.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        self.preview_frame.grid_columnconfigure(0, weight=1)
        self.preview_frame.grid_rowconfigure(0, weight=1)

        self.tree_preview = ttk.Treeview(self.preview_frame, show="headings")
        self.tree_preview.grid(row=0, column=0, sticky="nsew")

        v_scrollbar = ttk.Scrollbar(self.preview_frame, orient="vertical", command=self.tree_preview.yview)
        h_scrollbar = ttk.Scrollbar(self.preview_frame, orient="horizontal", command=self.tree_preview.xview)
        self.tree_preview.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)

        v_scrollbar.grid(row=0, column=1, sticky="ns")
        h_scrollbar.grid(row=1, column=0, sticky="ew")

    def update_dashboard(self):
        metrics = self.pipeline.review_integrity()
        self.render_summary_view(metrics)
        self.render_columns_view(metrics["col_stats"])
        self.render_preview_view()

    def render_summary_view(self, metrics):
        for widget in self.summary_frame.winfo_children():
            widget.destroy()

        # Simplified to numeric KPI data metrics only
        kpis = [
            ("Total Rows", metrics["total_rows"]),
            ("Total Columns", metrics["total_cols"]),
            ("Duplicate Records", f"{metrics['duplicate_count']} ({metrics['duplicate_pct']})"),
            ("Missing Cells", f"{metrics['total_nulls']} ({metrics['null_pct']})"),
            ("Text Placeholders", metrics["placeholder_count"])
        ]

        # Grid positions clean map layout linearly across a balanced 5 column split
        for idx, (title, value) in enumerate(kpis):
            card = ctk.CTkFrame(self.summary_frame, corner_radius=8, border_width=1)
            card.grid(row=0, column=idx, padx=6, pady=10, sticky="nsew")

            ctk.CTkLabel(card, text=title, font=("Arial", 11, "bold"), text_color="gray").pack(pady=(8, 2))
            ctk.CTkLabel(card, text=str(value), font=("Arial", 13, "bold"), justify="center").pack(pady=(2, 8))

        # Adjust the Matplotlib distribution map chart layout row position slightly
        fig, ax = plt.subplots(figsize=(7, 2.8)) 
        fig.patch.set_facecolor('#242424')
        ax.set_facecolor('#242424')

        if self.pipeline.df is not None and not self.pipeline.df.empty:
            sns.heatmap(self.pipeline.df.isnull(), cbar=False, yticklabels=False, cmap="viridis", ax=ax)

        ax.set_title("Missing Value Matrix Distribution Map", color="white", fontsize=11, pad=10)
        ax.tick_params(colors='white', labelsize=8, rotation=45)
        fig.tight_layout()

        canvas = FigureCanvasTkAgg(fig, master=self.summary_frame)
        canvas.draw()
        #canvas.get_tk_widget().grid(row=1, column=0, columnspan=5, pady=15, sticky="nsew")

        canvas_widget = canvas.get_tk_widget()
        canvas_widget.grid(row=1, column=0, columnspan=5, pady=(15, 10), padx=5, sticky="nsew")




    def render_columns_view(self, stats):
        for item in self.tree_cols.get_children():
            self.tree_cols.delete(item)
        for row in stats:
            self.tree_cols.insert("", "end", values=(
                row["column"], row["dtype"], row["null_count"], row["null_pct"], row["unique_count"]
            ))

    def run_transformations(self):
        try:
            # 1. Run the backend modifications and capture the text report
            log_output = self.pipeline.transform(
                placeholders=bool(self.chk_placeholders.get()),
                drop_duplicates=bool(self.chk_duplicates.get()),
                drop_nulls=bool(self.chk_nulls.get()),
                fill_nulls=True,  # Passing True triggers your backend mean/mode loop
                case_choice=self.case_var.get()
            )

            # 2. Save the log string directly onto the GUI class instance state
            self.last_imputation_log = log_output

            # 3. Update your terminal/textbox logger view
            self.txt_report.configure(state="normal")
            self.txt_report.delete("1.0", "end")
            self.txt_report.insert("1.0", log_output)
            self.txt_report.configure(state="disabled")

            # 4. Trigger the layout metrics recalculation
            self.btn_export.configure(state="normal")
            self.update_dashboard()

            messagebox.showinfo("Success", "Transformations executed and logged successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"Transformation pipeline crash:\n{str(e)}")



    def render_preview_view(self):
        df_sample = self.pipeline.preview(100)
        self.tree_preview["columns"] = list(df_sample.columns)
        for col in df_sample.columns:
            self.tree_preview.heading(col, text=col)
            self.tree_preview.column(col, anchor="w", width=130)

        for item in self.tree_preview.get_children():
            self.tree_preview.delete(item)

        for _, row in df_sample.iterrows():
            vals = ["" if pd.isna(v) else str(v) for v in row.values]
            self.tree_preview.insert("", "end", values=vals)

    def export_file(self):
        save_path = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV Document", "*.csv"), ("Excel Sheet", "*.xlsx")]
        )
        if not save_path:
            return
        try:
            self.pipeline.export(save_path)
            messagebox.showinfo("Export Status", "Refined file exported successfully!")
        except Exception as e:
            messagebox.showerror("Export Failure", f"Could not write target document onto storage drive:\n{str(e)}")

if __name__ == "__main__":
    app = ETLDashboardApp()
    app.mainloop()



# In[ ]:





# In[ ]:




