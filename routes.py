from flask import Blueprint, request, jsonify, render_template, redirect, flash, url_for
from flask_login import login_user, current_user, logout_user, login_required

api = Blueprint('api',__name__, url_prefix='/api')